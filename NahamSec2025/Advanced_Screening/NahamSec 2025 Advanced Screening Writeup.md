
![[Screenshots/Advanced_Screening_NHSec1.png]]

Started by taking a look at the website and seeing what points of entry are available and what I can glean.

![[Screenshots/Advanced_Screening_NHSec2.png]]

Taking a look using inspect in the firefox browser, I can see there is a piece of disabled code. Must be a way to enable it somehow...

Let's try entering an email and clicking the 'Request Access Code' button to see what happens
![[Screenshots/Advanced_Screening_NHSec3_2.png]]
![[Screenshots/Advanced_Screening_NHSec3_1.png]]

Taking a look at the networking tab, I see that when I attempt to enter my email I get a javascript pop up that says there was an error sending my email and in the networking tab I see where that request was sent. 

AN API. Let's try making a request to that endpoint directly and see what it may give us.

Connecting to it directly returned a response that said: "email is missing"

I am not going to start up ZAProxy and try giving it an email:

![[Screenshots/Advanced_Screening_NHSec4.png]]

I got an **ERROR** message! It says that only email addresses from 'movieservice.ctf' are allowed. So let's try 'admin@movieservice.ctf' as the email payload and see what happens:

![[Screenshots/Advanced_Screening_NHSec5_1.png]]![[Screenshots/Advanced_Screening_NHSec5_2.png]]

Verification email Sent!! Now we are getting somewhere!

Let's see if this enables the disabled code we saw earlier on the main page.

![[Screenshots/Advanced_Screening_NHSec6_1.png]]

![[Screenshots/Advanced_Screening_NHSec6_2.png]]

Look at that! We can see it now, and in the network tab it shows that the webapp has responded with an app.js file that seems to contain the backend logic. Let's go through it and see how this works.


![[Screenshots/Advanced_Screening_NHSec7.png]]

Looks like this works like a bad 2FA function. You give it an email, if it has the correct domain it will send you a 6 digit code. That code is then verified, and if it is correct then it will send a request to '/api/screen-token' with the 'user_id' as a json payload that it will then use to lookup a key which will then be used to redirect you to '/screen/?key=TOKENDATA'

Doesn't seem like we are gonna be easily able to get that six digit code since the code isn't actually sending an email to other domains. What if we just brute force the user_id's and attempt to get the screen-token directly?

Let's try that and see what happens:

![[Screenshots/Advanced_Screening_NHSec8.png]]

So connecting to it without the json payload gives us a message about something we already knew, so let's just use the proxy to make the request again, but this time inject the json payload. I don't know how these id's are formatted, but let's just start with the number 1 and see what happens. Id's are usually numbers and 1 is a number, so why not?

![[Screenshots/Advanced_Screening_NHSec9_1.png]]![[Screenshots/Advanced_Screening_NHSec9_2.png]]

WHOA! Well we didn't get a Token, but this tells us we are on the right track. It means we should try incrementing the user_id to see what other responses we get. 

I keep trying user_id's but so far 1-6 has given me 'Account deactivated' or 'User not found' messages, but we don't give up and just keep trying, let's try 7 now:

![[Screenshots/Advanced_Screening_NHSec10_1.png]]![[Screenshots/Advanced_Screening_NHSec10_2.png]]

THERE IT IS! We got a hash! Let's copy that down and make a request to the /screen/?key=TOKEN' endpoint and replace 'TOKEN' with the hash.

![[Screenshots/Advanced_Screening_NHSecFinal.png]]

And there is the FLAG! Not too bad. 