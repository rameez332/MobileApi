import requests

class Snap:
    def __init__(self, userName, passWord, loginWithMobile):
        ''' Initialize

        Initializes the class.
        '''
        self.api_url = 'https://mobileapi.snapdeal.com/service/'
        self.header = {'Content-Type': 'application/json; charset=utf-8'}
        self.session = self.getSession()
        self.userName = userName
        self.passWord = passWord
        self.loginWithMobile = loginWithMobile

    def getSession(self):
        ''' Session
		
        Create a session to GET or POST data.
        '''
        session = requests.Session()
        return session

    def postLogin(self):
        '''Post Login Call

        Sign in to the server
        '''
        loginType = ''
        
        if self.loginWithMobile:
            url = self.api_url + 'user/login/v2/loginWithMobile/'
            loginType = 'mobileNumber'
        else:
            url = self.api_url + 'user/login/v2/loginWithEmail/'
            loginType = 'emailId'
        
        json_data = {"requestProtocol":"PROTOCOL_JSON","responseProtocol":"PROTOCOL_JSON",loginType:self.userName,"password":self.passWord,"apiKey":"snapdeal"}
        
        login_response = self.session.post(url, json = json_data, headers = self.header)
        self.login_token = login_response.headers.get('Login-Token')
        return login_response

    def postLogout(self):
        '''Post Sign Out call

        Sign out from the server
        '''
        url = self.api_url + 'signout/'
        
        json_data = {'loginToken':self.login_token}
        return self.session.post(url, json = json_data, headers = self.header)

    def addToCart(self, pinCode, vendorCode, supc, catalogId, qty):
        '''Addition to Cart

        Add the product to Cart
        '''
        url = self.api_url + 'nativeCart/v2/insertItemToCart'
        
        json_data = {"pincode":"110025","items":[{"vendorCode":vendorCode,"supc":supc,"catalogId":catalogId
                     ,"quantity":qty}],"loginToken":self.login_token}
        
        cart_response = self.session.post(url, json = json_data, headers = self.header)

        if cart_response.json().get('successful'):
            print(''.join(cart_response.json().get('messages')))
        else:
            print('Product was not added, something went wrong')


    def valLogin(self):
        '''Validates Login Session

        Validates that login was successful
        '''
        login_response = self.postLogin()
        if login_response.json().get('status') == 'SUCCESS':
            print('You are Successfully Logged in')
            return True
        else:
            print('Something went wrong\n')
            print(login_response.json().get('exceptions')[0].get('errorMessage'))
            print('\nLogin Again\n')
            return False

    def valLogout(self):
        '''Validates Logout Session

        Validates that Logout was successful
        '''
        logout_response = self.postLogout()
        if logout_response.json().get('status') == 'true':
            print('You are Successfully Logged out....')
        else:
            print(logout_response.json().get('code'))

            

#This function is used for input username and password.
def inputUserData():
    loginWithMobile = True
    while(True): 
        userName = input('Please enter your Registered Username of Snapdeal\n')
        if userName.isdigit and len(userName) == 10:
            loginWithMobile = True
            break
        elif '@' in userName:
            loginWithMobile = False
            break
        else:
            print('\nPlease enter valid Username\n')
            print('--'*40)
    
    userPassword = input('Please enter your current Password\n')
    return (userName, userPassword, loginWithMobile)

#This function is used to set product details.
def setCart():
    pincode = ''
    while(True):
        pinCode = input('Please enter pincode for adding product to Cart\n')
        if len(pinCode) == 6 and pinCode.isdigit():
            break
        else:
            print('Please enter Valid Pincode')

    #Product Details.
    vendorCode = 'S667db'
    supc = 'SDL044719313'
    catalogId = 643083255133
    qty = 1
    print('\nFor the demo, the vendorCode, supc, catalogId and quantity are harcoded to \n{0}, {1}, {2} and {3} respectively\n'.format(vendorCode, supc, str(catalogId), str(qty)))

    return (pinCode, vendorCode, supc, catalogId, qty)


#Details of the Task given.
def taskDetails():
    print('--'*40)
    print('\n'+'Task Details'.center(60,' ')+'\n')
    print(' 1. Login into snapdeal using it\'s API\n')
    print(' 2. Add any product to cart using API\n')
    print(' 3. Logout from snapdeal\n')
    print('--'*40)


#Main class for all other functions.
def main():
    
    snap = None
    check = True
    
    #task details function
    taskDetails()
    
    while(check):

        userData = inputUserData()
        
        print('--'*40)
        
        #Initializing the Snap Class.
        snap = Snap(*userData)
        
        print('Validating your Credentials.........\n')
        #Login and validates the input data.
        check = not(snap.valLogin())
        print('--'*40)
    

    # Adding Product to Cart.
    cartData = setCart()
        
    print('Adding Product to Cart\n')
    snap.addToCart(*cartData)

    #Signing out the user
    print('--'*40)
    print('\nFinally signing out.........\n')
    snap.valLogout()


if __name__ == '__main__':
    main()
