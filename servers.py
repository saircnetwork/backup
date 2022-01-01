"""
servers.py
Contains information about the servers that should be backed up
"""

servers = {
        "ca-1.sa-irc.com": {
                "mysql": True,
                "host": "ca-1.sa-irc.com",
                "user": "backups"
        },
        "fr-2.sa-irc.com": {
                "mysql": True,
                "host": "fr-2.sa-irc.com",
                "user": "backups"
        },
        "lu-1.sa-irc.com": {
                "mysql": False,
                "host": "lu-1.sa-irc.com",
                "user": "backups"
        },
        "nl-1.sa-irc.com": {
                "mysql": True,
                "host": "nl-1.sa-irc.com",
                "user": "backups"
        },
        "uk-1.sa-irc.com": {
                "mysql": False,
                "host": "uk-1.sa-irc.com",
                "user": "backups"
        },
        "uk-2.sa-irc.com": {
                "mysql": False,
                "host": "uk-2.sa-irc.com",
                "user": "backups"
        },
        "uk-3.sa-irc.com": {
                "mysql": False,
                "host": "uk-3.sa-irc.com",
                "user": "backups"
        },
        "us-2.sa-irc.com": {
                "mysql": False,
                "host": "us-2.sa-irc.com",
                "user": "backups"
        },
        "us-3.sa-irc.com": {
                "mysql": False,
                "host": "us-3.sa-irc.com",
                "user": "backups"
        },
        "us-4.sa-irc.com": {
                "mysql": False,
                "host": "us-4.sa-irc.com",
                "user": "backups"
        }
}
