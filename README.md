# FoodieCallAPI
backend for foodiecall application

##  FoodieCallAPI
  # Base Urls
  * foodycallAPI/v1/auth/
  * foodycallAPI/v1/events/
  
  # Expanded Urls (authentication) 
  # POST
  * ^foodiecallAPI/v1/auth/ ^login/
    * link to login with login credentials 
  * ^foodiecallAPI/v1/auth/ ^token-refresh/
    * link to refresh token, obtain new token
  * ^foodiecallAPI/v1/auth/ ^token-verify/
    * verifies token is an unexpired/existing token
  * ^foodiecallAPI/v1/auth/ ^register/$
    * registers user body must include
      * email
      * username
      * mobile 
      * first_name
      * last_name
      * password
      * confirm_password
  * ^foodiecallAPI/v1/auth/ ^obtain-token/
    * obtains token with mobile and password
  # Expanded Urls (Events)
  * ^foodiecallAPI/v1/events/ ^events/
    * Post
      * Creates new event 
      * body must include
        * date_of_event
        * event_name
    * Get
      * As of now returns all events in DB in the future will only return events that have been created or attended by user
  * ^foodiecallAPI/v1/events/ ^events/$
    * Get
      * returns detais of event $
  * ^foodiecallAPI/v1/events/ ^events/<int:pk>/images/
    * Post
      * posts images to event pk if event pk was created by user 
      * body must include
        * image (char link to image)
    * Get
      * returns images of event pk
  * ^foodiecallAPI/v1/events/ events/<int:pk>/attendees/
    * Post
      * adds users to event pk only user who created event can add(invite) users to event pk
      * body must include
        * user (mobile number of user being invited)
    * Get
      * returns users invited to event pk
  * ^foodiecallAPI/v1/events/ events/<int:pk>/attendeeUpdate/
    * PUT
      * if user was invited to event pk user sends put request to update is_going field to true, or leaves at false
  * ^foodiecallAPI/v1/events/ events/<int:event_pk>/images/<int:image_pk>/vote/
    * Post
      * post a vote to image_pk in event event_pk

  

