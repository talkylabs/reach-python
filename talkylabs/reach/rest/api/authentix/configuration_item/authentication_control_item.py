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

from talkylabs.reach.base.instance_resource import InstanceResource
from talkylabs.reach.base.list_resource import ListResource
from talkylabs.reach.base.version import Version



class AuthenticationControlItemInstance(InstanceResource):

    """
    :ivar appletId: The identifier of the applet.
    :ivar apiVersion: The API version.
    :ivar configurationId: The identifier of the configuration.
    :ivar authenticationId: The identifier of the authentication.
    :ivar status: The outcome of the authentication control.
    :ivar dest: The phone number or email being verified. Phone numbers must be in E.164 format.
    :ivar channel: The channel used.
    :ivar paymentInfo: 
    :ivar dateCreated: The date and time in GMT that the authentication was created. 
    :ivar dateUpdated: The date and time in GMT that the authentication was last updated. 
    """

    def __init__(self, version: Version, payload: Dict[str, Any], configuration_id: str):
        super().__init__(version)

        
        self.appletId: Optional[str] = payload.get("appletId")
        self.apiVersion: Optional[str] = payload.get("apiVersion")
        self.configurationId: Optional[str] = payload.get("configurationId")
        self.authenticationId: Optional[str] = payload.get("authenticationId")
        self.status: Optional[str] = payload.get("status")
        self.dest: Optional[str] = payload.get("dest")
        self.channel: Optional[str] = payload.get("channel")
        self.paymentInfo: Optional[str] = payload.get("paymentInfo")
        self.dateCreated: Optional[datetime] = deserialize.iso8601_datetime(payload.get("dateCreated"))
        self.dateUpdated: Optional[datetime] = deserialize.iso8601_datetime(payload.get("dateUpdated"))

        
        self._solution = { 
            "configuration_id": configuration_id,
        }
        
    
    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Reach.Api.Authentix.AuthenticationControlItemInstance {}>'.format(context)

    def __str__(self) -> str:
        """
        Provide a str representation

        :returns: str representation
        """
        repr = { 
            'appletId': self.appletId,
            'apiVersion': self.apiVersion,
            'configurationId': self.configurationId,
            'authenticationId': self.authenticationId,
            'status': self.status,
            'dest': self.dest,
            'channel': self.channel,
            'paymentInfo': self.paymentInfo,
            'dateCreated': self.dateCreated,
            'dateUpdated': self.dateUpdated,
        }
        return serialize.serialize(repr)




class AuthenticationControlItemList(ListResource):

    def __init__(self, version: Version, configuration_id: str):
        """
        Initialize the AuthenticationControlItemList

        :param version: Version that contains the resource
        :param configuration_id: The identifier of the configuration being used.
        
        """
        super().__init__(version)

        
        # Path Solution
        self._solution = { 'configuration_id': configuration_id,  }
        
        self._uri = '/authentix/v1/configurations/{configuration_id}/authentication-controls'.format(**self._solution)
        
        
        
    
    def check(self, dest: Union[str, object]=values.unset, code: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, payment_info: Union[str, object]=values.unset) -> AuthenticationControlItemInstance:
        """
        Check the AuthenticationControlItemInstance

        :param dest: The phone number or email being authenticated. Phone numbers must be in E.164 format. Either this parameter or the `authenticationId` must be specified.
        :param code: The 4-10 character string being verified. This is required for `sms` and `email` channels.
        :param authentication_id: The ID of the authentication being checked. Either this parameter or the to `dest` must be specified.
        :param payment_info: Information related to the digital payment to authenticate. It is required when `usedForDigitalPayment` is true. It is ignored otherwise. It is a stringfied JSON map where keys are `payee`, `amount`, and `currency` and the associated values are respectively the payee, the amount, and the currency of a financial transaction. 
        
        :returns: The checked AuthenticationControlItemInstance
        """
        data = values.of({ 
            'dest': dest,
            'code': code,
            'authenticationId': authentication_id,
            'paymentInfo': payment_info,
        })
        
        payload = self._version.check(method='POST', uri=self._uri, data=data,)

        return AuthenticationControlItemInstance(self._version, payload, configuration_id=self._solution['configuration_id'])

    async def check_async(self, dest: Union[str, object]=values.unset, code: Union[str, object]=values.unset, authentication_id: Union[str, object]=values.unset, payment_info: Union[str, object]=values.unset) -> AuthenticationControlItemInstance:
        """
        Asynchronously check the AuthenticationControlItemInstance

        :param dest: The phone number or email being authenticated. Phone numbers must be in E.164 format. Either this parameter or the `authenticationId` must be specified.
        :param code: The 4-10 character string being verified. This is required for `sms` and `email` channels.
        :param authentication_id: The ID of the authentication being checked. Either this parameter or the to `dest` must be specified.
        :param payment_info: Information related to the digital payment to authenticate. It is required when `usedForDigitalPayment` is true. It is ignored otherwise. It is a stringfied JSON map where keys are `payee`, `amount`, and `currency` and the associated values are respectively the payee, the amount, and the currency of a financial transaction. 
        
        :returns: The checked AuthenticationControlItemInstance
        """
        data = values.of({ 
            'dest': dest,
            'code': code,
            'authenticationId': authentication_id,
            'paymentInfo': payment_info,
        })
        
        payload = await self._version.check_async(method='POST', uri=self._uri, data=data,)

        return AuthenticationControlItemInstance(self._version, payload, configuration_id=self._solution['configuration_id'])
    



    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return '<Reach.Api.Authentix.AuthenticationControlItemList>'

