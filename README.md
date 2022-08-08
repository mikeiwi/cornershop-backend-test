## Main Objective

We need a system to coordinate the meal delivery for Cornershop employees. Menus should be created by an admin user, while employees should be able to select their preferred menu option for the day.

The system should be highly manageable by admins and easy to use by employees, thanks to a slack integration.


## Requirements

* Only admin users may create menus for a specific date, as long as:
    * Current date and time is lower than the specific date at 9AM CLT (reminder sending time)
    * No menu exists for the specific date (one menu per day).
* Only admin users may edit menus for a specific date, as long as:
    * Current date and time is lower than the specific date at 9AM CLT (reminder sending time)
* A menu may contain multiple meal options. At least one option should be provided.
* Given a menu for the current day, a slack reminder should be sent to a specific Slack channel at 9 AM CLT automatically. This reminder should contain a “Menu of the day” link with the following pattern: [https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx](https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
* Given a “Menu of the day” link, a public page should be opened when clicked. In this page an employee may choose their preferred meal by providing this info:
    * Preferred menu option.
    * Optional customization for the meal. \
 \
To complete the checkout successfully, the employee should get authenticated or create an account. All in the same flow process.
* Only one meal option may be registered by an employee for a given day. 
* Only admin users should be able to see what employees requested for a given menu.


## Use Cases

These use cases should be implemented either in web pages or asynchronous actions.

![Use cases diagram](/docs/assets/use-cases.png)



## High Level System Design

Our application servers will manage our admins’ sessions and employees’ requests for choosing menu options. Due to the low expected usage (200-500 persons per office), one server might be enough to handle all requests during high traffic hours. But in case we expand and support more offices, we should be able to scale the application servers horizontally when needed.

A Worker server will communicate with a message Broker system to inform to run scheduled tasks. Worker will then be in charge of sending menu reminders to Slack asynchronously. 

![High level diagram](/docs/assets/high-level-diagram.png)


## Database Diagram
![Database schema](/docs/assets/database.png)


We need to store menus and their meals. Meals should be unique to avoid duplication.
A meal choice for an employee should be unique for a given menu.


## Checkout Process

An employee choosing a meal option for a menu should go through a checkout process with multiple steps:
* Time validation: checking if order is processable at the moment (menu exists and current time before 11 AM CLT)
* Is new order: an employee may have only one order per menu

In case the user is not already logged in, some other steps should be added:
* Can authenticate: user should provide credentials (username and password) and the system should check if it is possible to authenticate with those credentials.
* Is new user: if authentication fails, it could be due to a new employee requesting his/her first ever order. The system should check if the user is new or not.
* User signup: if the user doesn’t exist, a new user should be created.

There are some considerations regarding these previous steps (checks):

* Some of the previous checks are completely unrelated. 
* Flow may also change depending on the context of the request (if the user is authenticated, if the user exists). Two different request may take different paths.
* A request may be stopped (responded) by some of the checks, without needing to finish the entire flow.

With these considerations in mind a good way to implement this functionality is a hierarchical chain of responsibility for the two types of request: 

![Checkout flows diagram](/docs/assets/checkout-flows.png)


## Avoiding Meal Duplication

What are the chances that a meal for a day does not get repeated in a few days? Nora's team of chefs have to be the most creative cooks on the planet in order to come out with different menus every day.

It’s way more probable that a lot of meal options will be featuring multiple menus along the year, so we better take care of that. 

To solve this we are going to check the name of the Meal every time a new menu is created. If a Meal with the provided name already exists, it will be related to the menu instead of registering a new Meal.

This is far from a perfect solution. A better way could be adding a text search for meals on Menu creation, so Nora could look for already existing meals. Most popular meals could also be suggested during the creation of the menu. These solutions require a lot of UX functionalities, so they will not be implemented in this solution.


## Menu Reminder

Reminders will be sent asynchronously by a Worker. Everyday a task will run at 9 AM CLT looking for the menu of the current day. When found the Worker app will send a reminder to a slack channel with the menu link.

In order to accomplish this we need to create a Slack app with **channels:write** scope granted.

After that you need to get the “Bot User OAuth Token” and the channel ID you want to send the messages to. These two should be set as environment variables:

`SLACK_BOT_TOKEN`
`SLACK_CHANNEL_ID`


## Running and building the environment

### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000


### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.
So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```
# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test
make down
```

2- Give permissions to your system users to use Docker

```
## Where ${USER} is your current user
sudo usermod -aG docker ${USER}
```

3- Confirm current user is in docker group

```
## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.
id -nG
```


4-  Get the current user id

```
## Commonly your user id number is near to 1000
id -u
```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment 

```
make rebuild
make up
```
