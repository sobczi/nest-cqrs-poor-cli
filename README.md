# nest-cqrs-poor-cli
Python script that support creating new working directory for NestCQRS which is same as in the [orginal docs](https://docs.nestjs.com/recipes/cqrs). 

## Commands
***m User***

Creates cqrs working directory.

![Screenshot](resources/module.jpg)


***c/q/e example-name***

Creates command/query/event implementation and handler, pins it to appropriate array of (Command||Query||Event)Handlers.

## Personalization
In the code you can find `MODIFICABLE` section where you can set additional sequential `imports` and declarations for constructors `c_args` or functions `hf`.  Index `0` belongs to implementation part, `1` to the handlers.

## Note
To get working creating commands/queries/event the directory must follow the offical pattern.
