import sys, os
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

action = sys.argv[1]
if action == 'm':
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
  }"""

  module_content = """import { Module } from '@nestjs/common';
  import { CqrsModule } from '@nestjs/cqrs';
  import { """+name+"""Controller } from './"""+name.lower()+""".controller';
  import { """+name+"""Model } from './models/"""+name.lower()+""".model';
  import { CommandHandlers } from './commands/handlers';
  import { QueryHandlers } from './queries/handlers';
  import { EventHandlers } from './events/handlers';

  @Module({
    imports: [CqrsModule],
    controllers: ["""+name+"""Controller],
    providers: [
      """+name+"""Model,
      ...CommandHandlers,
      ...QueryHandlers,
      ...EventHandlers
    ]
  })

  export class """+name+"""Module {}
  """

  model_content = """import { AggregateRoot } from '@nestjs/cqrs';

  export class """+name+"""Model extends AggregateRoot {
    constructor(

    ) { super(); }
  }
  """

  name2 = name
  v = name+"/"+name2.lower()+".controller.ts"
  controller = open(v,"w+")

  v = name+"/"+name2.lower()+".module.ts"
  module = open(v, "w+")

  v = name+"/models/"+name2.lower()+".model.ts"
  model = open(v,"w+")

  controller.write(controller_content)
  module.write(module_content)
  model.write(model_content)

  controller.close()
  module.close()
  model.close()
  print("Ready!")
elif action == 'c' or action == 'q' or action == 'e':
  directory = ""
  ext = ""
  imp1 = ""
  imp2 = ""
  name = sys.argv[2]
  namearr = name.split("-")
  capname = ""
  for i in range(len(namearr)):
    namearr[i] = namearr[i].capitalize()
    capname += namearr[i]
  #MODIFICABLE:
  hf = "" #function execute/handle
  c_args = [2] 
  c_args.append("") # [0] arguments constructor impl
  c_args.append("") # [1] arguments constructor handler
  imports = [2]
  imports.append("") # [0] additional imports impl
  imports.append("") # [1] additional imports handler
  if(action == 'c'): 
    print("Creating command..")
    directory = "commands"
    ext = "command"
    imp1 = "CommandHandler"
    imp2 = "ICommandHandler"
    hf = "async execute("+ext+": "+capname+ext.capitalize()+"){\n  }"
    c_args[0] = ""
    c_args[1] = ""
    imports[0] = ""
    imports[1] = ""
  elif action == 'q': 
    print("Creating query..")
    directory = "queries"
    ext = "query"
    imp1 = "QueryHandler"
    imp2 = "IQueryHandler"
    hf = "async execute("+ext+": "+capname+ext.capitalize()+"){\n  }"
    c_args[0] = ""
    c_args[1] = ""
    imports[0] = ""
    imports[1] = ""
  elif action == 'e': 
    print("Creating event..")
    directory = "events"
    ext = "event"
    imp1 = "EventsHandler"
    imp2 = "IEventHandler"
    hf = "handle("+ext+": "+capname+ext.capitalize()+"){\n  }"
    c_args[0] = ""
    c_args[1] = ""
    imports[0] = ""
    imports[1] = ""

  impl = "./"+directory+"/impl/"+name+"."+ext+".ts"
  impl_content = imports[0]+"""export class """+capname+ext.capitalize()+""" {
  constructor("""+c_args[0]+""") {} 
}"""
  f = open(impl, "w+")
  f.write(impl_content)
  f.close()

  handler = "./"+directory+"/handlers/"+name+".handler.ts"
  handler_content = """import { """+imp1+""","""+imp2+""" } from '@nestjs/cqrs';
import { """+capname+ext.capitalize()+""" } from '../impl/"""+name+"""."""+ext+"""';
"""+imports[1]+"""

@"""+imp1+"""("""+capname+ext.capitalize()+""")
export class """+capname+"""Handler implements """+imp2+"""<"""+capname+ext.capitalize()+""">{
  constructor("""+c_args[1]+""") {}
  """+hf+"""
}
  """
  f = open(handler,"w+")
  f.write(handler_content)
  f.close()
  indx = "./"+directory+"/handlers/index.ts"
  f = open(indx,"r")
  lines = f.readlines()
  new_lines = [];
  new_lines.append("import { "+capname+"Handler } from './"+name+".handler';\n")
  for i in range(len(lines)):
    x = re.sub("export const "+ext.capitalize()+"Handlers ?= ?\[\n?","export const "+ext.capitalize()+"Handlers = [\n  "+capname+"Handler,",lines[i])
    new_lines.append(x)
  nf = ''.join(new_lines)

  f = open(indx,"w+")
  f.writelines(nf)
  f.close()
  print("Ready!")
else: invalid()