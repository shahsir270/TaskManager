
# Task Manager

this a simple web application Api which helps users to create a task and associate it with a team.
The team leader of the team will assign the team member or team members to the task. The
team member will update the status of the task.

I Use Django as the project framework and Django rest framework for building RESTful API
and Use Celery for any background tasks and console backend for sending email.

You can clone this Api and use it for Your web application 



## API Reference


#### register user

```http
  POST  /auth/register/
```

#### login user

```http
  POST  /auth/login/

  message: it gives token and use this token for autherization
```
#### create Team

```http
  GET  /auth/create/team/
  message: it gives team leaders and team members details to create team

  POST  /auth/create/team/

  condition: only user can create team you need to login for do this action
```
#### create Task

```http
  GET  /create/task/
  message: it gives teams and team leaders details to create task

  POST  /create/task/

  condition: only user can create team you need to login for do this action

```
#### Update Task

```http
  GET  /update/<int:id>/task/
  message: it gives task with deatils

  POST  /update/<int:id>/task/

  condition: only team_leader can update task details
```
#### Update Status of Task 

```http
  GET   /status/update/<int:id>/task/
  message: it gives status of Task to change

  POST  /status/update/<int:id>/task/

  condition: only team_members can change this task
```
#### Task List

```http
  GET  /
  message: it gives all task which are created

  condition: only autherized user can see this details 
```



## Usage

It's best to install Python projects in a Virtual Environment. Once you have set up a VE, clone this project

```
 git clone https://github.com/adigunsherif/Django-School-Management-System.git
```

Then install django and celery and configure it in your system after that

```
  cd TaskManager
```

Run

```
  pip install -r requirements.txt #install required packages
  python manage.py migrate # run first migration
  python manage.py runserver # run the server
```
