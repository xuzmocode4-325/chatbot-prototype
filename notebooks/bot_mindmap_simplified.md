```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#52dea0',
      'primaryTextColor': '#0f3849',
      'primaryBorderColor': '#6ecef2',
      'lineColor': '#008cef',
      'secondaryColor': '#ffff',
      'tertiaryColor': '#6ccbef'
    }
  }
}%%

flowchart LR;
    id0((User)) === id1[Prompt];

    id1 ===  API ==> | Guardrails | id2[Framework\n Agent Executor] 
   
    id2 ==>| Context | LLM
    LLM  ===> | Guardrails | id7{Response} 

    id3 --- id2
    id3{{Embedding\n Model}} 
    id4[Data\n Documents] -.- id3
    id5[(Vectore\n Database)] -.- id3
    id6(((Web Search))) -.- id3
    
    id7 ==> id0

```
