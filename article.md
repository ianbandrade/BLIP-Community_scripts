[[_TOC_]]

# Introduction

This script was made by the need to reset all **WhatsApp** users who had their last interaction with the service until a date x.

***Note**: can be easily adapted to others channels.*

# Installation

To run the script, you need to install Python. The latest version can be downloaded [here](https://www.python.org/downloads/).

We can also install Python using [Chocolatey](https://chocolatey.org/) (package manager for windows), through PowerShell. Just use the command below (it is necessary to run the PowerShell as administrator):

```bash
choco install python
```

## Libraries

After install Python, one library was used to normalize the user phone numbers. And the library with version is:

- phonenumbers==8.12.39

# Running

To run the script you can just pass the arguments as console parameters following the order below.

## Parameters

 | **Parameter**                  | **Description**             |
 | ------------------------------ | --------------------------- |
 | SUB_BOT_AUTHORIZATION          | Subbot authorization key    |
 | ROUTER_AUTHORIZATION           | Router authorization key    |
 | ORGANIZATION                   | Organization of the service |
 | DATE (using format DD/MM/YYYY) | Last interaction date       |

 ***Note:** the authorization keys need to be passed without the `Key` word.*

 If you need to pickup just the router contacts or just the subbot contacts, just equalize the authorizations keys.  

## Example

```py
python .\reset_state_id_before_date.py Ym1ncm91dGVyYmV0YTpwaTRpbHRaT3U2UjM1OW04bnFGOQ== Ym1ncm91dGVyYmV0YTpwaTRpbHRaT3U2UjM1OW04bnFGOQ== bancobmg 10/11/2021
```
