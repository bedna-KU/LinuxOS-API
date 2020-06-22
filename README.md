# LinuxOS-API
## In development
This is not really API only few scripts for download data from https://linuxos.sk/ and save it to user_themes_comments.txt

`losAPI-user_themes_comments.py`
Download all commented themes by user

`losAPI-user_all_comments.py`
Download all comments by user (you need to run losAPI-user_themes_comments.py first)

`losAPI-user_all_qa.py`
Download all comments if have parent (you need to run losAPI-user_themes_comments.py first)

Save to two files comments_user.txt and comments_parent.txt

`losAPI.py` Now only get users without posts
