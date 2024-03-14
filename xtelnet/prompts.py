    # if the default method didn't work out, then change the values inside those lists to reach your goal!!!
class Telnet_Prompts:
    # expected login prompts ( don't forget the: "b" before the expected string )
    login = [
        b"User:",
        b"user:",
        b"User>",
        b"user>",
        b"Name:",
        b"sername:",
        b"name:",
        b"Name>",
        b"sername>",
        b"name>",
        b"ogin:",
        b"ogin>",
        b"assword:",
        b"Pass:",
        b"pass:",
        b"nter>",
        b"asswd:",
        b"assword>",
        b"asswd>",
        b"pass>",
        b"Pass>",
    ]

    # expected login failing prompts
    fail = [
        "expired",
        "invalid",
        "wrong",
        "failed",
        "incorrect",
        "bad",
        "denied",
        "closed",
        "user:",
        "user>",
        "username:",
        "name:",
        "username>",
        "name>",
        "login:",
        "login>",
        "password:",
        "pass:",
        "passwd:",
        "password>",
        "passwd>",
        "pass>",
    ]

    # expected username prompts
    user = [
        "user:",
        "user>",
        "username:",
        "username>",
        "name:",
        "name>",
        "login:",
        "login>",
    ]

    # expected password prompts
    password = ["password:", "password>", "pass:", "pass>", "passwd:", "passwd>"]

    # expected anti-bot prompts
    enter = ["press return", "press enter", "enter>"]

    # expected ends of shell's prompt
    shell = ["$", "#", ">", "%", "]"]
