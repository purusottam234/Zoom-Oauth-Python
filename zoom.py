import base64
import requests
from  django.conf import settings


class ZoomOAuth:
    """
    Zoom OAuth 2.0
    ~~~~~~~~~~~~~~

    Zoom OAuth 2.0 is a protocol that allows developers to
    authenticate users via a third-party service.

    This class defines few methods to get the access token.
    """
    __client_id = settings.ClientID
    __client_secret = settings.ClientSecret
    __auth_url = 'https://zoom.us/oauth/'
    __redirect_uri = settings.Zoom_Redirect_URI

    def __init__(self) -> None:
        self.id_secret_encrypted = base64.b64encode(
            (self.__client_id + ':' + self.__client_secret).encode('utf-8')).decode('utf-8')

    def request_authorization_code(self):
        """
        This method is used to request the authorization code.
        """

        params = {
            "client_id": self.__client_id,
            "response_type": "code",
            "redirect_uri": self.__redirect_uri,
            # "state": "12345",  # Optional
        }
        url = self.__auth_url+'authorize'+'?' + \
            '&'.join(['='.join([k, v]) for k, v in params.items()])

        # Direct User to this url. This will ask the user to authorize the app.
        # If authorized, the user will be redirected to the redirect_uri with authorization code in the code query parameter.
        # example: https://[redirect_uri]/?code=obBEe8ewaL_KdyNjniT4KPd8ffDWt9fGB
        return url

    def get_first_token(self, code):
        """
        This method is used to get the access token
        after the user has authorized the app.

        Required field is code.

        Returns:
            If successful, the Response Body will be a JSON
            response containing the user's access token.

            {
                "access_token": "YOUR_ACCESS_TOKEN",
                "token_type": "Bearer",
                "refresh_token": "YOUR_REFRESH_TOKEN",
                "expires_in": 3600,
                "scope": "user:read user:write"
            }
        """

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + self.id_secret_encrypted
        }
        params = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.__redirect_uri,
        }
        response = requests.post(
            self.__auth_url+'token', headers=headers, params=params)
        return response

    def get_access_token(self, refresh_token):
        """
        This method is used to get the new access token using refresh_token.
        Refresh tokens expire after 15 years.
        The latest refresh token must always be used for the next refresh request.

        Returns:
            If successful, the Response Body will be a JSON
            response containing the user's access token.

            {
                "access_token": "YOUR_ACCESS_TOKEN",
                "token_type": "Bearer",
                "refresh_token": "YOUR_REFRESH_TOKEN",
                "expires_in": 3600,
                "scope": "user:read user:write"
            }
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + self.id_secret_encrypted
        }
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(
            self.__auth_url+'token', headers=headers, params=params)
        return response

    def revoke_token(self, access_token):
        """
        This method is used to revoke the access token.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + self.id_secret_encrypted
        }
        params = {
            "token": access_token,
        }
        response = requests.post(
            self.__auth_url+'revoke', headers=headers, params=params)
        return response


class ZoomAPI:
    """
    Zoom API
    ~~~~~~~~

    This class let you access the Zoom APIs.
    API endpoint = https://api.zoom.us/v2/

    Full API documentation: https://marketplace.zoom.us/docs/api-reference/contact-center/methods
    """
    __api_url = 'https://api.zoom.us/v2/'

    # def create_user(self, refresh_token, action, first_name, last_name, email, password, type=1):
    #     """
    #     This method is used to create a user.
    #     Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Users/operation/userCreate
    #     """
    #     headers = {
    #         'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
    #     }
    #     data = {
    #         "action": action,
    #         "first_name": first_name,
    #         "last_name": last_name,
    #         "email": email,
    #         "password": password,
    #         "type": type
    #     }
    #     response = requests.post(
    #         self.__api_url+'users', headers=headers, json=data)
    #     return response

    def get_user_zak(self, refresh_token):
        """
        This method is used to get the user's Zoom Access Key (ZAK).
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Users/operation/userZak

        returns:
        {
            "token": "YOUR_ZAK"
        }
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.get(
            self.__api_url+'users/me/zak', headers=headers)
        return response

    def create_meeting(self, refresh_token, meeting_name, start_time, duration, timezone, agenda, settings, type=2):
        """
        This method is used to create a meeting.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meetingCreate
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        data = {
            "topic": meeting_name,
            "start_time": start_time,
            "duration": duration,
            "timezone": timezone,
            "agenda": agenda,
            "settings": settings,
            "type": type
        }
        response = requests.post(
            self.__api_url+'users/me/meetings', headers=headers, json=data)
        return response

    def get_meetings(self, refresh_token):
        """
        This method is used to get the list of meetings.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meetings
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.get(
            self.__api_url+'users/me/meetings', headers=headers)
        return response

    def get_meeting_details(self, refresh_token, meeting_id):
        """
        This method is used to get the details of a meeting.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meeting
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.get(
            self.__api_url+'meetings/'+meeting_id, headers=headers)
        return response

    def delete_meeting(self, refresh_token, meeting_id):
        """
        This method is used to delete a meeting.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meetingDelete
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.delete(
            self.__api_url+'meetings/'+meeting_id, headers=headers)
        return response

    def update_meeting(self, refresh_token, meeting_id, meeting_name, start_time, duration, timezone, agenda, recurrence, settings, type=2):
        """
        This method is used to update a meeting.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meetingUpdate
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        data = {
            "topic": meeting_name,
            "start_time": start_time,
            "duration": duration,
            "timezone": timezone,
            "agenda": agenda,
            "recurrence": recurrence,
            "settings": settings,
            "type": type
        }
        response = requests.put(
            self.__api_url+'meetings/'+meeting_id, headers=headers, json=data)
        return response

    def update_meeting_status(self, refresh_token, meeting_id, status):
        """
        This method is used to update a meeting.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Meetings/operation/meetingStatus
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        data = {
            "status": status
        }
        response = requests.put(
            self.__api_url+'meetings/'+meeting_id, headers=headers, json=data)
        return response

    def list_users(self, refresh_token):
        """
        This method is used to get the list of users.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Users/operation/users
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.get(
            self.__api_url+'users', headers=headers)
        return response

    def get_user_details(self, refresh_token, user_id):
        """
        This method is used to get the details of a user.
        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Users/operation/user
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        response = requests.get(
            self.__api_url+'users/'+user_id, headers=headers)
        return response

    def check_user_email(self, refresh_token, email):
        """
        This method is used to check if a user exists.

        ```Note```: You can successfully check if a user is a
        registered Zoom user only if the user ```signed up
        for Zoom via email and is within your account.```
        If you provide an email address of a user who is
        not in your account, the value of "existed_email"
        parameter will be "false" irrespective of whether
        or not the user is registered with Zoom.
        The response of this API call will not include
        users who joined Zoom using options such as
        "Sign in with SSO", "Sign in with Google" or
        "Sign in with Facebook" even if they are in
        the same account as yours.

        Link - https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Users/operation/userEmail
        """
        headers = {
            'Authorization': 'Bearer ' + ZoomOAuth().get_access_token(refresh_token=refresh_token).json()['access_token']
        }
        data = {
            "email": email
        }
        response = requests.get(
            self.__api_url+'users/email', headers=headers, json=data)
        return response
