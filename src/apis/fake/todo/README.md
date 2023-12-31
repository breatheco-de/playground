# TodoList API

---

⚠️ The use of [Postman](https://www.getpostman.com/downloads/) or [Insomnia (recomended)](https://insomnia.rest/) is strongly recomended for testing the API.

<br/>

## How to use this API:

1. Create your todolist with `[POST] /todos/user/<username>`. (you can pick any username)
2. Update your todolist with `[PUT] /todos/user/<username>`, you have to pass the whole todolist every time.
3. Delete your todolist (if needed) `[DELETE] /todos/user/<username>`.

<br/>

## 1. Get list of todo's for a particular user


      [GET] /user/<username>
          Content-Type: "application/json"
          PARAMS: None

      RESPONSE:

          [
              { id:"3694a48ec",  label: "Make the bed", done: false },
              { id:"c34b4dbb8b",  label: "Walk the dog", done: false },
              { id:"0611f8fdc",  label: "Do the replits", done: false}
          ]

<br/>

## 2. Create a new todo list of a particular user

This method is only for creation, you need to pass an empty array on the body because there are no todo yet.


      [POST] /todos/user/<username>
          Content-Type: "application/json"
          BODY: []

      RESPONSE:
          {
              "result": "ok"
          }

<br/>

## 3. Update `the entire list` of todo's of a particular user

This method is to update only, if you want to create a new todo list for a particular user use the POST above.


      [PUT] /todos/user/<username>
          Content-Type: "application/json"
          BODY:
              [
                  { label: "Make the bed", done: false },
                  { label: "Walk the dog", done: false },
                  { label: "Do the replits", done: false }
              ]

      RESPONSE:
          {
              "result": "A list with 3 todos was succesfully saved"
          }

<br/>

## 4. Delete a user and all of their todo's

      [DELETE] /todos/user/<username>
          Content-Type: "application/json"
          PARAMS: none

      RESPONSE:

          [ "result": "ok" ]
