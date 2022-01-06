from requests import Session
from uuid import uuid4
from datetime import datetime
import phonenumbers
import sys

SUB_BOT_AUTHORIZATION = ''
ROUTER_AUTHORIZATION = ''
ORGANIZATION = ''
DATE = ''

RESET_STATE_URL = 'https://flowassistant.hmg-cs.blip.ai/api-states'

SKIP_ZERO = 0
FIXED_SKIP = 99
COUNTER = 0

GET_METHOD = 'get'
DELETE_METHOD = 'delete'

COUNTRY_CODE = "BR"
USERS = []

DELETED_USERS = []
NOT_DELETED_USERS = []


def request_contacts_body(num_of_contacts):
    return {
        'id': str(uuid4()),
        'method': GET_METHOD,
        'uri': f'/contacts?$skip={num_of_contacts}'
    }


def get_contacts_by_page(session, skip):
    body = request_contacts_body(skip)
    response = session.post(COMMANDS_URL, json=body)
    response = response.json()

    return response['resource']['items']


def get_number_of_contacts(session):
    body = request_contacts_body(SKIP_ZERO)
    response = session.post(COMMANDS_URL, json=body)
    response = response.json()

    return response['resource']['total']


def delete_user_master_state(identity):
    session = Session()

    result = session.delete(RESET_STATE_URL,
                            headers={
                                'Organization': ORGANIZATION,
                                'ContactIdentity': identity,
                                'BotAuthorization': ROUTER_AUTHORIZATION
                            })

    if(result.status_code == 500):
        NOT_DELETED_USERS.append(identity)
    else:
        DELETED_USERS.append(identity)


def filter_users_by_access_date(users):
    date = datetime.strptime(DATE, '%d/%m/%Y')
    iso_date = date.isoformat() + '.000Z'
    for user in users:
        if (str(user.get('lastMessageDate')) < iso_date and user.get('phoneNumber')):
            if (len(user['phoneNumber']) < 14):
                USERS.append(user['phoneNumber'])


def generate_user_contact_identity():
    users = []

    for user in USERS:
        phoneNumber = phonenumbers.parse(user, COUNTRY_CODE)
        contact_identity = f'{phoneNumber.country_code}{phoneNumber.national_number}@wa.gw.msging.net'
        users.append(contact_identity)

    return users


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            f'use: python {__file__} <SUB_BOT_AUTHORIZATION> <ROUTER_AUTHORIZATION> <ORGANIZATION> <DATE(D/M/Y)>')
        exit(-1)

    SUB_BOT_AUTHORIZATION = f'Key {sys.argv[1]}'
    ROUTER_AUTHORIZATION = f'Key {sys.argv[2]}'
    ORGANIZATION = sys.argv[3]
    DATE = sys.argv[4]

    COMMANDS_URL = f'https://{ORGANIZATION}.http.msging.net/commands'

    session = Session()
    session.headers = {
        'Authorization': SUB_BOT_AUTHORIZATION
    }
    total_of_contacts = get_number_of_contacts(session=session)

    rest = total_of_contacts % FIXED_SKIP
    iterations = total_of_contacts // FIXED_SKIP

    while COUNTER < total_of_contacts:
        if rest != 0:
            COUNTER = rest
            rest = 0
        else:
            COUNTER += FIXED_SKIP

        users = get_contacts_by_page(session=session, skip=COUNTER)
        filter_users_by_access_date(users)

    USERS = generate_user_contact_identity()

    for user in USERS:
        delete_user_master_state(user)

    if NOT_DELETED_USERS:
        print('\x1b[6;30;41m' +
              'The following identities could not have their identities be deleted: \n' + '\x1b[0m')
        for notDeletedUser in NOT_DELETED_USERS:
            print(notDeletedUser, end="\n")\

    if DELETED_USERS:
        print('\n' + '\x1b[6;30;42m' +
              'The following identities contexts were deleted successfully: \n' + '\x1b[0m')
        for deletedUsers in DELETED_USERS:
            print(deletedUsers, end="\n")
