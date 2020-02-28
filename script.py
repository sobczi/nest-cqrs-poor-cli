import sys
import os
import re


def invalid():
  print("""Arguments usage (py script.py || script.exe)...:
  m Example - creates cqrs working directory
    ./Example/
      /commands
        /handlers
          index.ts
        /impl
      /events
        /handlers
          index.ts
        /impl
      /queries
        /handlers
          /index.ts
        /impl
      /models
        example.model.ts
      example.controller.ts
      example.module.ts

  c example-name - creates ExampleNameCommand and ExampleNameHandler
    creates:
    ./
      /commands
        /handlers
          example-name.handler.ts
        /impl
          example-name.command.ts
    modifies:
    ./
      /commands
        /handlers
          index.ts => 
          import { ExampleNameHandler } from './example-name.handler';
          const export CommandHandlers = [***ExampleNameHandler,***]

  q example-name - creates ExampleNameQuery and ExampleNameHandler = same logic but for ./queries and QueryHandlers
  e example-name - creates ExampleNameEvent and ExampleNameHandler = same logic but for ./events and EventHandlers

  to get it working it need to be run in directory tree same as produced by this script
  """)


if len(sys.argv) < 3:
  invalid()
  sys.exit()

#MODULE
action = sys.argv[1]
if action == 'm':
  #Custom Module
  CUSTOM_IMPORTS = ""
  #!End with comma
  CUSTOM_MODULES = ""
  CUSTOM_CONTROLLERS = ""
  CUSTOM_PROVIDERS = ""

  print("Creating module..")
  name = sys.argv[2]
  name = name.capitalize()

  commands = name+"/commands/"
  events = name+"/events/"
  queries = name+"/queries/"

  models = name+"/models/"
  handlers = [commands, events, queries]
  indexs = [
      'export const CommandHandlers = [];',
      'export const EventHandlers = [];',
      'export const QueryHandlers = [];'
  ]

  for i in range(len(handlers)):
    v = handlers[i]+"impl/"
    os.makedirs(v)

    v = handlers[i]+"handlers/"
    os.makedirs(v)

    v = handlers[i]+"handlers/index.ts"
    f = open(v, "w+")
    f.write(indexs[i])
    f.close()

  os.makedirs(models)

  controller_content = """import { Controller } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';

@Controller()
export class """+name+"""Controller {
  constructor(
    private readonly commandBus: CommandBus,
    private readonly queryBus: QueryBus
  ) { }
} """

  module_content = CUSTOM_IMPORTS+"""import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { """+name+"""Controller } from './"""+name.lower()+""".controller';
import { """+name+"""Model } from './models/"""+name.lower()+""".model';
import { CommandHandlers } from './commands/handlers';
import { QueryHandlers } from './queries/handlers';
import { EventHandlers } from './events/handlers';

@Module({
  imports: ["""+CUSTOM_MODULES+"""CqrsModule],
  controllers: ["""+CUSTOM_CONTROLLERS+name+"""Controller],
  providers: [
    """+CUSTOM_PROVIDERS+"""
    """+name+"""Model,
    ...CommandHandlers,
    ...QueryHandlers,
    ...EventHandlers
  ]
})

export class """+name+"""Module {}
"""

  model_content = """import { AggregateRoot } from '@nestjs/cqrs';
import { RepositoryService } from 'src/shared/services/repo.service';
  
export class """+name+"""Model extends AggregateRoot {
  constructor(
    private readonly body: any,
    private readonly service: RepositoryService
  ) { super(); }
}
  """

  name2 = name
  v = name+"/"+name2.lower()+".controller.ts"
  controller = open(v, "w+")

  v = name+"/"+name2.lower()+".module.ts"
  module = open(v, "w+")

  v = name+"/models/"+name2.lower()+".model.ts"
  model = open(v, "w+")

  controller.write(controller_content)
  module.write(module_content)
  model.write(model_content)

  controller.close()
  module.close()
  model.close()
  print("Ready!")
### Command || Query || Event
elif action == 'c' or action == 'q' or action == 'e':
  ext = "command"
  if action == 'q': ext = "query"
  elif action == 'e': ext = "event"
  name = sys.argv[2]
  namearr = name.split("-")
  capname = ""
  for i in range(len(namearr)):
    namearr[i] = namearr[i].capitalize()
    capname += namearr[i]
#CUSTOM HANDLER_FUNCTION
  #Execute (Commands,Queries) or Handle (Events)
  #Index will be choosen below based on action
  #C stands for Commands - Index 0
  #Q stands for Queries - Index 1
  #E stands for Events - Index 2
  HANDLER_FUNCTION = [""] * 3
  #execute function of ExampleCommandHandler
  HANDLER_FUNCTION[0] = """async execute("""+ext+""": """+capname+ext.capitalize()+"""){

  }"""
  #execute function of ExampleQueryHandler
  HANDLER_FUNCTION[1] = """async execute("""+ext+""": """+capname+ext.capitalize() + """){

  }"""
  #handle function of ExampleEventHandler
  HANDLER_FUNCTION[2] = """handle("""+ext+""": """+capname+ext.capitalize() + """){

  }"""

#CUSTOM IMPORTS
  #Index 0 stand for implemantation part
  #Index 1 stands for handler part
  CUSTOM_IMPORTS = [["" for i in range(2)] for j in range(3)]
  #Imports for Commands
  #Example1Command
  CUSTOM_IMPORTS[0][0] = ""
  #Example1Handler
  CUSTOM_IMPORTS[0][1] = ""
  
  #Imports for Queries
  #Example2Query
  CUSTOM_IMPORTS[1][0] = ""
  #Example2Handler
  CUSTOM_IMPORTS[1][1] = ""

  #Imports for Events
  CUSTOM_IMPORTS[2][0] = ""
  CUSTOM_IMPORTS[2][1] = ""

#CUSTOM CONSTRUCTOR_ARGUMENTS
  #Index 0 stands for implementation part
  #Index 1 stands for handler part
  CONSTRUCTOR_ARGUMENTS = [["" for i in range(2)] for j in range(3)]
  #Arguments for Commands
  #Example1Command
  CONSTRUCTOR_ARGUMENTS[0][0] = ""
  #Example1Handler
  CONSTRUCTOR_ARGUMENTS[0][1] = ""

  #Arguments for Queries
  #Example2Query
  CONSTRUCTOR_ARGUMENTS[1][0] = ""
  #Example2Handler
  CONSTRUCTOR_ARGUMENTS[1][1] = ""

  #Arguments for Events
  #Example3Event
  CONSTRUCTOR_ARGUMENTS[2][0] = ""
  #Example3Handler
  CONSTRUCTOR_ARGUMENTS[2][1] = ""


#DO NOT CHANGE, NEED TO WORK
  #IMPORTS
  STANDARD_IMPORT = ["" for j in range(3)]
  #Imports for Command
  STANDARD_IMPORT[0] = "import { CommandHandler,ICommandHandler } from '@nestjs/cqrs';"
  #Import for Queries
  STANDARD_IMPORT[1] = "import { QueryHandler,IQueryHandler } from '@nestjs/cqrs';"
  #Import for Events
  STANDARD_IMPORT[2] = "import { EventsHandler,IEventHandler } from '@nestjs/cqrs';"

  #DECLARATIONS
  STANDARD_DECLARATIONS = [["" for i in range(2)] for j in range(3)]
  #Declarations for Command
  STANDARD_DECLARATIONS[0][0] = "CommandHandler"
  STANDARD_DECLARATIONS[0][1] = "ICommandHandler"
  #Declarations for Queries
  STANDARD_DECLARATIONS[1][0] = "QueryHandler"
  STANDARD_DECLARATIONS[1][1] = "IQueryHandler"
  #Declarations for Events
  STANDARD_DECLARATIONS[2][0] = "EventsHandler"
  STANDARD_DECLARATIONS[2][1] = "IEventHandler"

  #DIRECTORIES AND EXTENSIONS
  DIRECTORIES = ["commands","queries","events"]
  EXTENSIONS = ["command","query","event"]

  #CHOOSEN ELEMENTS
  CHOOSEN_HANDLER_FUNCTION = CHOOSEN_STANDARD_IMPORT = CHOOSEN_DIRECTORY = CHOOSEN_EXTENSION = ""
  CHOOSEN_CONSTRUCTOR_ARGUMENTS = [""] * 2
  CHOOSEN_CUSTOM_IMPORTS = [""] * 2
  CHOOSEN_DECLARATIONS = [""] * 2
  if(action == 'c'):
    print("Creating command..")
    CHOOSEN_HANDLER_FUNCTION = HANDLER_FUNCTION[0]
    CHOOSEN_CONSTRUCTOR_ARGUMENTS = CONSTRUCTOR_ARGUMENTS[0]
    CHOOSEN_STANDARD_IMPORT = STANDARD_IMPORT[0]
    CHOOSEN_CUSTOM_IMPORTS = CUSTOM_IMPORTS[0]
    CHOOSEN_DECLARATIONS = STANDARD_DECLARATIONS[0]
    CHOOSEN_DIRECTORY = DIRECTORIES[0]
    CHOOSEN_EXTENSION = EXTENSIONS[0]
  elif action == 'q':
    print("Creating query..")
    CHOOSEN_HANDLER_FUNCTION = HANDLER_FUNCTION[1]
    CHOOSEN_CONSTRUCTOR_ARGUMENTS = CONSTRUCTOR_ARGUMENTS[1]
    CHOOSEN_STANDARD_IMPORT = STANDARD_IMPORT[1]
    CHOOSEN_CUSTOM_IMPORTS = CUSTOM_IMPORTS[1]
    CHOOSEN_DECLARATIONS = STANDARD_DECLARATIONS[1]
    CHOOSEN_DIRECTORY = DIRECTORIES[1]
    CHOOSEN_EXTENSION = EXTENSIONS[1]
  elif action == 'e':
    print("Creating event..")
    CHOOSEN_HANDLER_FUNCTION = HANDLER_FUNCTION[2]
    CHOOSEN_CONSTRUCTOR_ARGUMENTS = CONSTRUCTOR_ARGUMENTS[2]
    CHOOSEN_STANDARD_IMPORT = STANDARD_IMPORT[2]
    CHOOSEN_CUSTOM_IMPORTS = CUSTOM_IMPORTS[2]
    CHOOSEN_DECLARATIONS = STANDARD_DECLARATIONS[2]
    CHOOSEN_DIRECTORY = DIRECTORIES[2]
    CHOOSEN_EXTENSION = EXTENSIONS[2]

#WRITING IMPLEMENTATION PART
  impl = "./"+CHOOSEN_DIRECTORY+"/impl/"+name+"."+CHOOSEN_EXTENSION+".ts"
  impl_content = CHOOSEN_CUSTOM_IMPORTS[0]+"""export class """+capname+CHOOSEN_EXTENSION.capitalize()+""" {
  constructor("""+CHOOSEN_CONSTRUCTOR_ARGUMENTS[0]+""") {} 
}"""
  f = open(impl, "w+")
  f.write(impl_content)
  f.close()

#WRITING HANDLER PART
  handler = "./"+CHOOSEN_DIRECTORY+"/handlers/"+name+".handler.ts"
  handler_content = CHOOSEN_CUSTOM_IMPORTS[1]+CHOOSEN_STANDARD_IMPORT+"""
import { """+capname+CHOOSEN_EXTENSION.capitalize()+""" } from '../impl/"""+name+"""."""+CHOOSEN_EXTENSION+"""';

@"""+CHOOSEN_DECLARATIONS[0]+"""("""+capname+CHOOSEN_EXTENSION.capitalize()+""")
export class """+capname+"""Handler implements """+CHOOSEN_DECLARATIONS[1]+"""<"""+capname+CHOOSEN_EXTENSION.capitalize()+""">{
  constructor("""+CHOOSEN_CONSTRUCTOR_ARGUMENTS[1]+""") {}
  """+CHOOSEN_HANDLER_FUNCTION+"""
}
  """

  f = open(handler, "w+")
  f.write(handler_content)
  f.close()

#WRITING INDEX PART
  index_file = "./"+CHOOSEN_DIRECTORY+"/handlers/index.ts"
  f = open(index_file, "r")
  lines = f.readlines()

  new_lines = []
  new_lines.append("import { "+capname+"Handler } from './"+name+".handler';\n")

  for i in range(len(lines)):
    x = re.sub("export const "+CHOOSEN_EXTENSION.capitalize() +
      "Handlers ?= ?\[\n?", "export const "+CHOOSEN_EXTENSION.capitalize()+"Handlers = [\n  "+capname+"Handler,", lines[i])
    new_lines.append(x)
  new_file_lines = ''.join(new_lines)

  f = open(index_file, "w+")
  f.writelines(new_file_lines)
  f.close()

  print("Ready!")
else:
  invalid()
