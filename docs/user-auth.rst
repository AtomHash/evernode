.. _user-auth:

User Authentication
===================

This section will cover the basics of user authentication in EverNode.

Simple Usage
----------------

Below is an example of how to use the UserAuth class. UserAuth has a method called :code:`session()`
which returns a JWT token that is stored into the database. The config.json has an option called
:code:`FAST_SESSIONS` which just turns off database validation. It is recommended in a production/
high security enviroment to turn this option to false. This protects users from sessions that have
been hijacked, because if the session is removed from the database the session is no longer valid.
The JWT token is encrypted by the :code:`SERECT` string set in your config.json, then encrypted by
your :code:`KEY` string. For :code:`FAST_SESSIONS` tokens to be valid it must be decrypted without
error and not expired. The validity period is set in seconds by :code:`JWT_EXP_SECS` config.json
setting.

| **UserAuth Class**
| class: :class:`evernode.classes.UserAuth`

::

    from evernode.classes import UserAuth
    from evernode.models import BaseUserModel

    userAuth = UserAuth(
            BaseUserModel,
            username_error='Please enter your email',  # username empty
            password_error='Please enter your password')  # password empty
        session = userAuth.session()
        if session is None:
            # return a 400 bad request HTTP status, password incorrect/username incorrect
            return JsonResponse(400)
        # return 200 successful HTTP status with a authorization token
        return JsonResponse(200, None, session)