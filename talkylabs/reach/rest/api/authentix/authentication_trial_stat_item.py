r"""
    This code was generated by
  ___ ___   _   ___ _  _    _____ _   _    _  ___   ___      _   ___ ___      ___   _   ___     ___ ___ _  _ ___ ___    _ _____ ___  ___ 
 | _ \ __| /_\ / __| || |__|_   _/_\ | |  | |/ | \ / / |    /_\ | _ ) __|___ / _ \ /_\ |_ _|__ / __| __| \| | __| _ \  /_\_   _/ _ \| _ \
 |   / _| / _ \ (__| __ |___|| |/ _ \| |__| ' < \ V /| |__ / _ \| _ \__ \___| (_) / _ \ | |___| (_ | _|| .` | _||   / / _ \| || (_) |   /
 |_|_\___/_/ \_\___|_||_|    |_/_/ \_\____|_|\_\ |_| |____/_/ \_\___/___/    \___/_/ \_\___|   \___|___|_|\_|___|_|_\/_/ \_\_| \___/|_|_\
 
    Reach Authentix API
     Reach Authentix API helps you easily integrate user authentification in your application. The authentification allows to verify that a user is indeed at the origin of a request from your application.  At the moment, the Reach Authentix API supports the following channels:    * SMS      * Email   We are continuously working to add additionnal channels. ## Base URL All endpoints described in this documentation are relative to the following base URL: ``` https://api.reach.talkylabs.com/rest/authentix/v1/ ```  The API is provided over HTTPS protocol to ensure data privacy.  ## API Authentication Requests made to the API must be authenticated. You need to provide the `ApiUser` and `ApiKey` associated with your applet. This information could be found in the settings of the applet. ```curl curl -X GET [BASE_URL]/configurations -H \"ApiUser:[Your_Api_User]\" -H \"ApiKey:[Your_Api_Key]\" ``` ## Reach Authentix API Workflow Three steps are needed in order to authenticate a given user using the Reach Authentix API. ### Step 1: Create an Authentix configuration A configuration is a set of settings used to define and send an authentication code to a user. This includes, for example: ```   - the length of the authentication code,    - the message template,    - and so on... ``` A configuaration could be created via the web application or directly using the Reach Authentix API. This step does not need to be performed every time one wants to use the Reach Authentix API. Indeed, once created, a configuartion could be used to authenticate several users in the future.    ### Step 2: Send an authentication code A configuration is used to send an authentication code via a selected channel to a user. For now, the supported channels are `sms`, and `email`. We are working hard to support additional channels. Newly created authentications will have a status of `awaiting`. ### Step 3: Verify the authentication code This step allows to verify that the code submitted by the user matched the one sent previously. If, there is a match, then the status of the authentication changes from `awaiting` to `passed`. Otherwise, the status remains `awaiting` until either it is verified or it expires. In the latter case, the status becomes `expired`. 

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from talkylabs.reach.base import deserialize, serialize, values
from talkylabs.reach.base.instance_context import InstanceContext
from talkylabs.reach.base.instance_resource import InstanceResource
from talkylabs.reach.base.list_resource import ListResource
from talkylabs.reach.base.version import Version



class AuthenticationTrialStatItemInstance(InstanceResource):

    """
    :ivar appletId: The identifier of the applet.
    :ivar apiVersion: The API version.
    :ivar totalTrials: The total number of trials matching the specified criteria.
    :ivar numSuccessfulTrials: The total number of successfull trials among the ones matching the specified criteria.
    :ivar numUnsuccessfulTrials: The total number of unsuccessfull trials among the ones matching the specified criteria.
    :ivar successRate: The success rate of the trials matching the specified criteria.
    """

    def __init__(self, version: Version, payload: Dict[str, Any]):
        super().__init__(version)

        
        self.appletId: Optional[str] = payload.get("appletId")
        self.apiVersion: Optional[str] = payload.get("apiVersion")
        self.totalTrials: Optional[int] = deserialize.integer(payload.get("totalTrials"))
        self.numSuccessfulTrials: Optional[int] = deserialize.integer(payload.get("numSuccessfulTrials"))
        self.numUnsuccessfulTrials: Optional[int] = deserialize.integer(payload.get("numUnsuccessfulTrials"))
        self.successRate: Optional[float] = deserialize.decimal(payload.get("successRate"))

        
        self._context: Optional[AuthenticationTrialStatItemContext] = None

    @property
    def _proxy(self) -> "AuthenticationTrialStatItemContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: AuthenticationTrialStatItemContext for this AuthenticationTrialStatItemInstance
        """
        if self._context is None:
            self._context = AuthenticationTrialStatItemContext(self._version,)
        return self._context
    
    
    def fetch(self, dest: Union[str, object]=values.unset, trial_status: Union[str, object]=values.unset, channel: Union[str, object]=values.unset, configuration_id: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, country: Union[str, object]=values.unset, sent_at: Union[datetime, object]=values.unset, sent_after: Union[datetime, object]=values.unset, sent_before: Union[datetime, object]=values.unset) -> "AuthenticationTrialStatItemInstance":
        """
        Fetch the AuthenticationTrialStatItemInstance
        
        :param dest: Filter authentication trials sent only to this phone number or email. The phone number must be in the E.164 format.
        :param trial_status: Filter authentication trials with the specified status.
        :param channel: Filter authentication trials sent via the specified channel.
        :param configuration_id: Filter authentication trials from the configuration whose ID matches the specified one.
        :param authentication_id: Filter authentication trials from the authentication whose ID matches the specified one.
        :param country: Filter authentication trials sent to the specified destination country (in ISO 3166-1 alpha-2). Only possible when `dest` is a phone number.
        :param sent_at: Filter authentication trials created at the specified date. Must be in ISO 8601 format.
        :param sent_after: Filter authentication trials created after the specified datetime. Must be in ISO 8601 format.
        :param sent_before: Filter authentication trials created before the specified datetime. Must be in ISO 8601 format.

        :returns: The fetched AuthenticationTrialStatItemInstance
        """
        return self._proxy.fetch(dest=dest, trial_status=trial_status, channel=channel, configuration_id=configuration_id, authentication_id=authentication_id, country=country, sent_at=sent_at, sent_after=sent_after, sent_before=sent_before, )

    async def fetch_async(self, dest: Union[str, object]=values.unset, trial_status: Union[str, object]=values.unset, channel: Union[str, object]=values.unset, configuration_id: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, country: Union[str, object]=values.unset, sent_at: Union[datetime, object]=values.unset, sent_after: Union[datetime, object]=values.unset, sent_before: Union[datetime, object]=values.unset) -> "AuthenticationTrialStatItemInstance":
        """
        Asynchronous coroutine to fetch the AuthenticationTrialStatItemInstance
        
        :param dest: Filter authentication trials sent only to this phone number or email. The phone number must be in the E.164 format.
        :param trial_status: Filter authentication trials with the specified status.
        :param channel: Filter authentication trials sent via the specified channel.
        :param configuration_id: Filter authentication trials from the configuration whose ID matches the specified one.
        :param authentication_id: Filter authentication trials from the authentication whose ID matches the specified one.
        :param country: Filter authentication trials sent to the specified destination country (in ISO 3166-1 alpha-2). Only possible when `dest` is a phone number.
        :param sent_at: Filter authentication trials created at the specified date. Must be in ISO 8601 format.
        :param sent_after: Filter authentication trials created after the specified datetime. Must be in ISO 8601 format.
        :param sent_before: Filter authentication trials created before the specified datetime. Must be in ISO 8601 format.

        :returns: The fetched AuthenticationTrialStatItemInstance
        """
        return await self._proxy.fetch_async(dest=dest, trial_status=trial_status, channel=channel, configuration_id=configuration_id, authentication_id=authentication_id, country=country, sent_at=sent_at, sent_after=sent_after, sent_before=sent_before, )
    
    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        
        return '<Reach.Api.Authentix.AuthenticationTrialStatItemInstance>'

    def __str__(self) -> str:
        """
        Provide a str representation

        :returns: str representation
        """
        repr = { 
            'appletId': self.appletId,
            'apiVersion': self.apiVersion,
            'totalTrials': self.totalTrials,
            'numSuccessfulTrials': self.numSuccessfulTrials,
            'numUnsuccessfulTrials': self.numUnsuccessfulTrials,
            'successRate': self.successRate,
        }
        return serialize.serialize(repr)

class AuthenticationTrialStatItemContext(InstanceContext):

    def __init__(self, version: Version):
        """
        Initialize the AuthenticationTrialStatItemContext

        :param version: Version that contains the resource
        """
        super().__init__(version)

        
        
        
        self._uri = '/authentix/v1/authenticationTrialStats'
        
        
    
    
    def fetch(self, dest: Union[str, object]=values.unset, trial_status: Union[str, object]=values.unset, channel: Union[str, object]=values.unset, configuration_id: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, country: Union[str, object]=values.unset, sent_at: Union[datetime, object]=values.unset, sent_after: Union[datetime, object]=values.unset, sent_before: Union[datetime, object]=values.unset) -> AuthenticationTrialStatItemInstance:
        """
        Fetch the AuthenticationTrialStatItemInstance
        
        :param dest: Filter authentication trials sent only to this phone number or email. The phone number must be in the E.164 format.
        :param trial_status: Filter authentication trials with the specified status.
        :param channel: Filter authentication trials sent via the specified channel.
        :param configuration_id: Filter authentication trials from the configuration whose ID matches the specified one.
        :param authentication_id: Filter authentication trials from the authentication whose ID matches the specified one.
        :param country: Filter authentication trials sent to the specified destination country (in ISO 3166-1 alpha-2). Only possible when `dest` is a phone number.
        :param sent_at: Filter authentication trials created at the specified date. Must be in ISO 8601 format.
        :param sent_after: Filter authentication trials created after the specified datetime. Must be in ISO 8601 format.
        :param sent_before: Filter authentication trials created before the specified datetime. Must be in ISO 8601 format.

        :returns: The fetched AuthenticationTrialStatItemInstance
        """
        
        data = values.of({ 
            'dest': dest,
            'trialStatus': trial_status,
            'channel': channel,
            'configurationId': configuration_id,
            'authenticationId': authentication_id,
            'country': country,
            'sentAt': serialize.iso8601_datetime(sent_at),
            'sentAfter': serialize.iso8601_datetime(sent_after),
            'sentBefore': serialize.iso8601_datetime(sent_before),
        })
        
        payload = self._version.fetch(method='GET', uri=self._uri, params=data)

        return AuthenticationTrialStatItemInstance(
            self._version,
            payload,
            
        )

    async def fetch_async(self, dest: Union[str, object]=values.unset, trial_status: Union[str, object]=values.unset, channel: Union[str, object]=values.unset, configuration_id: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, country: Union[str, object]=values.unset, sent_at: Union[datetime, object]=values.unset, sent_after: Union[datetime, object]=values.unset, sent_before: Union[datetime, object]=values.unset) -> AuthenticationTrialStatItemInstance:
        """
        Asynchronous coroutine to fetch the AuthenticationTrialStatItemInstance
        
        :param dest: Filter authentication trials sent only to this phone number or email. The phone number must be in the E.164 format.
        :param trial_status: Filter authentication trials with the specified status.
        :param channel: Filter authentication trials sent via the specified channel.
        :param configuration_id: Filter authentication trials from the configuration whose ID matches the specified one.
        :param authentication_id: Filter authentication trials from the authentication whose ID matches the specified one.
        :param country: Filter authentication trials sent to the specified destination country (in ISO 3166-1 alpha-2). Only possible when `dest` is a phone number.
        :param sent_at: Filter authentication trials created at the specified date. Must be in ISO 8601 format.
        :param sent_after: Filter authentication trials created after the specified datetime. Must be in ISO 8601 format.
        :param sent_before: Filter authentication trials created before the specified datetime. Must be in ISO 8601 format.

        :returns: The fetched AuthenticationTrialStatItemInstance
        """
        
        data = values.of({ 
            'dest': dest,
            'trialStatus': trial_status,
            'channel': channel,
            'configurationId': configuration_id,
            'authenticationId': authentication_id,
            'country': country,
            'sentAt': serialize.iso8601_datetime(sent_at),
            'sentAfter': serialize.iso8601_datetime(sent_after),
            'sentBefore': serialize.iso8601_datetime(sent_before),
        })
        
        payload = await self._version.fetch_async(method='GET', uri=self._uri, params=data)

        return AuthenticationTrialStatItemInstance(
            self._version,
            payload,
            
        )
    
    
    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        
        return '<Reach.Api.Authentix.AuthenticationTrialStatItemContext>'



class AuthenticationTrialStatItemList(ListResource):

    def __init__(self, version: Version):
        """
        Initialize the AuthenticationTrialStatItemList

        :param version: Version that contains the resource
        
        """
        super().__init__(version)

        
        
        
        
        
        

    def get(self) -> AuthenticationTrialStatItemContext:
        """
        Constructs a AuthenticationTrialStatItemContext
        
        """
        return AuthenticationTrialStatItemContext(self._version)

    def __call__(self) -> AuthenticationTrialStatItemContext:
        """
        Constructs a AuthenticationTrialStatItemContext
        
        """
        return AuthenticationTrialStatItemContext(self._version)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return '<Reach.Api.Authentix.AuthenticationTrialStatItemList>'

