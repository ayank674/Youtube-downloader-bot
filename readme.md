# A YT DOWNLOADER TELEGRAM BOT.

## DISCLAIMER: Do Not Use This Bot To Infringe Anyone's Copyright.

## USAGE:

### General commands

- start: check if bot is alive.
- download: reply to a youtube link and follow the directions. A demo is attached below:

### Admin only commands.

- add_user: reply to a user's id.

### Owner only commands.

- add_admin: reply to a user's id.
- display_users: returns a list of users.
- display_users: returns a list of admins.
- remove_user: removes a user/admin.

## TO DEPLOY:

- Create a [render](render.com) account.
- Visit render's [New Web Service](https://dashboard.render.com/select-repo?type=web) Page.
- Paste this [repo's link](https://github.com/VengeanceOG/Youtube-downloader-bot) in Public git repository option and click continue.
- Give a name to your service in the name placeholder.
- Go to advanced and add these variables:
  - OWNER (Your telegram user id.)
  - SESSION_NAME (Name of this bot's session.)
  - API_ID (Get this from [developer tools](https://my.telegram.org/apps))
  - API_HASH (Get this from [developer tools](https://my.telegram.org/apps))
  - BOT_TOKEN (Generate from @Botfather.)
  - CRASH_MESSAGE (A message to be displayed in case an error occurs.)
  - ENCRYPT_KEY (Generate using fernet.)
- Click on create web service and your bot would be live.
