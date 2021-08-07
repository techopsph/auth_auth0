# Auth0 module for Odoo

Forked for Odoo 14 from https://github.com/idazco/

This makes it simple to implement SSO with Auth0 in Odoo. While this module currently inherits from
the OAuth module available from the Odoo 10 CE release, we plan in future to make it a stand-alone module.
This is because Auth0 is an effective Authentication broker that makes it unnecessary to have the OAuth
configuration options offered in the standard module. Typically, one would use one or the other.

# Installation:

## Download and install

 1. Clone this project. The entire project is the module, so you can either clone it directly into your
 Odoo 10 add-ons folder or just link it to the add-ons folder.
 1. Go to the Apps list and remove the `Apps` filter in the search box since this module is a utility and not an app.
 1. Locate the `Auth0` module and install it.
 
**Tip:** If you need this module in a Docker image, you could add the following to your Dockerfile:
```
RUN wget https://github.com/idazco/odoo_auth0/archive/master.zip -O /tmp/tmp.zip
RUN unzip /tmp/tmp.zip -d /mnt/downloaded-addons/
RUN mv ./odoo_auth0-master ./auth0
RUN rm /tmp/tmp.zip
```
This will download the module and unzip it's source in the image to `/tmp/downloaded-addons`, which of course you
will need to add to the add-ons path in your Odoo config

### Python dependencies
If needed install pyjwt as follows:

    pip install pyjwt
 
## Configure

 1. In the Odoo Settings, activate the developer mode, then locate the `Auth0` link on the left menu list under `Users` and click it.
 1. In the `Provider Name` column, select the `Auth0` record anc click the `Edit` button to add your own settings.
 1. From your Auth0 account, configure a new [client](https://auth0.com/docs/clients) as a Regular Web Application,
 and add other settings for the client as needed such as the allowed callback URLs (refer to the Auth0 documentation for details)
 1. Take the Domain, Client ID, Client Secret and transfer them to the appropriate fields in the Odoo Auth0 settings.
 *Note:* As the text in `Authentication URL` and `Validation URL` fields indicate, simply replace the `[your-auth0-domain]`
 piece of the text in that field with the Domain from your Auth0 Client Settings.
 1. Finally check the "Allowed" check box and save the record.

## Use

*The type of connections you will use for your Auth0 client configuration are entirely up to you and setting that up is well
documented on Auth0.com and is therefore beyond the scope of this readme file. We will assume you already setup your Auth0 client
to use some sort of connection that has a valid account you can use going forward*

 1. Create a user account in Odoo that you intend to use with your Auth0 client connection (the email addresses must match).
 So for example, if my Auth0 client is configured with a Google social connection and I want to use the email 'john.doe@gmail.com',
 then the email address of the created user in Odoo must also be 'john.doe@gmail.com'.
 1. Log out of Odoo and go back to the sign in page (`/web/login`)
 1. You will notice that now there is a new link that says "Sign in with Auth0". Use that to sign in with the email address.
 
# Caveats, considerations and limitations

 - This module assumes that you will **always** intend to have the user authenticate with Auth0 SSO, therefore setting a password for
 the user in Odoo will not work. For security purposes and considering a broader scope of implementation than just social OAuth providers,
 this module will automatically create a new complex password for the user *each time* they use it to sign in. This means that if you set
 a password for the use in Odoo and the user then logs in with Auth0 SSO, that Odoo password will be wiped replaced. This is purposely done
 as a trade off between security and convenience. In the case of SSO connections using an LDAP backend auth provider the application is clear:
 If the user's account has been disabled in the LDAP server, the LDAP server won't allow them to authenticate and they are effectively blocked
 from getting into your Odoo database. However, if the Odoo administrator set an Odoo password for this user and gave it to them,
 they could still use that to login. Since logging in that way uses their Odoo login and password, they would effectively be bypassing
 LDAP authentication. **Not good.** This means that an administrator would have to remember to also disable their account or change their
 password in Odoo. Rather than relying on that paradigm, this module will instead make that situation impossible.
 So in a corporate environment for example, this means that an employee would just be deactivated in the
 directory (e.g. LDAP or Active Directory) and they will also not be able to get into the Odoo database.
 In the case of authenticating users with social connections, its also a good idea not to allow the user to set an Odoo password.
 Often, certain types of users will use one password everywhere and might then actually use the actual password for their social account in
 your Odoo database as well. This represents a terrible risk for the users and a possible liability for you.
 
 - At this time, this module does not validate the JWT signature provided by Auth0. As it currently is, the JWT signature is provided by Auth0
 through a request over an HTTPS connection using the Client Secret, which should be sufficiently secure to trust the JWT and not need to
 validate further. Keep in mind that before JWTs became popular, the typical OAuth paradigm would provide the web app with an *access token*
 which was explicitly trusted because of how it was provided and there was no additional step to validate the access token.
 JWTs have mostly replaced access tokens, but similarly, they could also be trusted because of how they are provided.
 Therefore this module does not implement JWT signature verification at this time.
  