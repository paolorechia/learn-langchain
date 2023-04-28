# learn-langchain

AI Agent with Vicuna

This repository is a playground that makes it easy to use Zero Shot / Few Shot prompts based on the ReAct framework, with LLama based models, such as Vicuna, with the langchain framework.

## Installation

Disclaimer: This may not be the most effective way to install, but it's how I've done.
It's possible that the installation process is not working as expected, and you might have to install additional requirements. If that's the case,
feel free to open a PR to fix it or an issue about it.

### NVIDIA Driver / Toolkit
First, install the NVIDIA toolkit: https://developer.nvidia.com/cuda-11-8-0-download-archive

In my case, I installed using the deb repository, which downloaded a CUDA toolkit 12.1

If you don't have a GPU, you should skip this, of course.

### Installing Python dependencies

Run, in your bash, run: 
```
chmod +x ./install_on_virtualenv_and_pip.sh 
./install_on_virtualenv_and_pip.sh`
```

If you're not running bash, and you don't have a virtualenv, or created it another way, 
you can execute the commands, adapting to your OS/shell:

```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install -r requirements.txt
```

Just note that might clobber your main Python installation, if possible, use a virtualenv!

### Git LFS for cloning quantized models
For the quantized models, you also need git lfs installed: https://git-lfs.com/


## Running the server

### Default Parameters
If you have the virtualenv, start it by running: `source learn-langchain/bin/activate`

Then:

```bash
uvicorn servers.vicuna_server:app 
```

**If you want to load a different model than the default:**

```
export USE_13B_MODEL=true && export USE_4BIT=true && uvicorn servers.vicuna_server:app

```

#### On Windows

If you've somehow managed to install everything on Windows (congrats!), please feel free to contribute to extend this README.md. So far we know that you need to follow this change:

```
Your command to use a different model returns an error if you try and run it on windows:

export USE_13B_MODEL=true && export USE_4BIT=true && uvicorn servers.vicuna_server:app

The export and && isn't supported. I found that you can use the set command and format it like this:

set USE_13B_MODEL=true; set USE_4BIT=true;uvicorn servers.vicuna_server:app
```

Thanks to @unoriginalscreenname for sharing

#### Downloading quantized models
When you run it for the first time, the server might throw you an error that the model is not found. You should follow the instruction, for instance, cloning:

```bash
git clone https://huggingface.co/TheBloke/vicuna-7B-1.1-GPTQ-4bit-128g
```

Make sure you have installed `git lfs` first. You can also run this command beforehand, if you know the version you want to use.

### Config (Update 25.04)
This repository has again been reorganized, adding support for 4 bit models (from gpqt_for_llama: https://github.com/qwopqwop200/GPTQ-for-LLaMa)

You can now change the server behavior by setting environment variables:

```python
class Config:
    def __init__(self) -> None:
        self.base_model_size = "13b" if os.getenv("USE_13B_MODEL") else "7b"
        self.use_for_4bit = True if os.getenv("USE_FOR_4BIT") else False
        self.use_fine_tuned_lora = True if os.getenv("USE_FINE_TUNED_LORA") else False
        self.lora_weights = os.getenv("LORA_WEIGHTS")
        self.device = "cpu" if os.getenv("USE_CPU") else "cuda"
        self.model_path = os.getenv("MODEL_PATH", "")
        self.model_checkpoint = os.getenv("MODEL_CHECKPOINT", "")
```

Some options are incompatible with each other, the code does not check for all possibilities.

This repository support the following models:

- Vicuna 7b unquantized, HF format (16-bits) - this is the default (https://huggingface.co/eachadea/vicuna-7b-1.1)
- Vicuna 7b LoRA fine-tune (8-bits)
- Vicuna 7b GPQT 4-bit group-size 128
- Vicuna 13b unquantized, HF format (16-bits)
- Vicuna 13b GPQT 4-bit group-size 128



## Examples

Note: The coding prompts are currently unreliable, and what works with model might not work with another.

### Cat Jokes
Using this to start server:

```bash
export USE_4BIT=true
export USE_13B_MODEL=true
uvicorn servers.vicuna_server:app 
```

You can get this output:

```bash
(learn-langchain) paolo@paolo-MS-7D08:~/learn-langchain$ python3 -m langchain_app.agents.cat_joke

> Entering new AgentExecutor chain...
I must use the Python REPL to write a script that generates cat jokes and saves them to a CSV file called 'catjokes.csv'.
Action: Python REPL
Action Input:
import csv # line 1
jokes = ["Why did the cat go to the vet?", "Because it was meowt!"] # line 2
with open("catjokes.csv", "w", newline="") as csvfile: # line 3
    writer = csv.writer(csvfile) # line 4
    writer.writerow(jokes) # line 5

Observation: 
Thought:I now know the answer
Final Answer: I have executed the task successfully.

Final Answer: I have executed the task successfully.

> Finished chain.
(learn-langchain) paolo@paolo-MS-7D08:~/learn-langchain$ cat catjokes.csv 
Why did the cat go to the vet?,Because it was meowt!
```

### Chuck Norris Prompt

Note: The original prompt from the article is not working anymore, as I might have modified something in the process.

The model that seems to perform better at this sort of task is the new WizardLM: https://huggingface.co/TheBloke/wizardLM-7B-HF

Server start. Modify the file 'run_server.sh' with this:
```
export MODEL_PATH=TheBloke/wizardLM-7B-HF
uvicorn servers.vicuna_server:app
```

```(learn-langchain) paolo@paolo-MS-7D08:~/learn-langchain$ python -m langchain_app.agents.chuck_norris_simple
> Entering new AgentExecutor chain...
I should use requests library to fetch the data from the API
Action: Python REPL
Action Input: 
import requests
Observation: 
Thought:I should define the endpoint URL
Action: Python REPL
Action Input: 
url = 'https://api.chucknorris.io/jokes/random'
Observation: 
Thought:I should send a GET request to the endpoint
Action: Python REPL
Action Input: 
response = requests.get(url)
Observation: 
Thought:I should check if the response status code is 200
Action: Python REPL
Action Input: 
if response.status_code == 200:
    # extract the joke from the response
    data = response.json()
    joke = data['value']
    print(joke)
else:
    print('Error fetching joke')
Observation: Chuck Norris once ran a one-minute mile. He did it dragging an 18-wheeler while running in a field of wet cement.

Thought:I have successfully fetched and printed the joke.
Final Answer: Chuck Norris once ran a one-minute mile. He did it dragging an 18-wheeler while running in a field of wet cement.

> Finished chain.
(learn-langchain) paolo@paolo-MS-7D08:~/learn-langchain$ 
```

### Answer about Germany Q/A

```python -m langchain_app.agents.answer_about_germany```


Sample output:

```text

Type your question: Where is Germany Located?


> Entering new AgentExecutor chain...
I should always think about what to do
Action: Search
Action Input: Germany
Observation: [(Document(page_content="'''Germany''',{{efn|{{lang-de|Deutschland}}, {{IPA-de|ˈdɔʏtʃlant|pron|De-Deutschland.ogg}}}} officially the '''Federal Republic of Germany''',{{efn|{{Lang-de|Bundesrepublik Deutschland}}, {{IPA-de|ˈbʊndəsʁepuˌbliːk ˈdɔʏtʃlant|pron|De-Bundesrepublik Deutschland.ogg}}<ref>{{cite book|title=Duden, Aussprachewörterbuch|publisher=Dudenverlag|year=2005|isbn=978-3-411-04066-7|editor-last=Mangold|editor-first=Max|edition=6th|pages=271, 53f|language=de}}</ref>}} is a country in [[Central Europe]]. It is the [[List of European countries by population|second-most populous country]] in Europe after [[Russia]], and the most populous [[member state of the European Union]]. Germany is situated between the [[Baltic Sea|Baltic]] and [[North Sea|North]] seas to the north, and the [[Alps]] to the south. Its 16 [[States of Germany|constituent states]] are bordered by [[Denmark]] to the north, [[Poland]] and the [[Czech Republic]] to the east, [[Austria]] and [[Switzerland]] to the south, and [[France]], [[Luxembourg]], [[Belgium]], and the [[Netherlands]] to the west. The nation's capital and [[List of cities in Germany by population|most populous city]] is [[Berlin]] and its main financial centre is [[Frankfurt]]; the largest urban area is the [[Ruhr]].", metadata={'source': '1'}), 0.8264833092689514)]
Thought:I now know the final answer
Final Answer: Germany is a country located in Central Europe, bordered by the Baltic and North seas to the north, the Alps to the south, and bordered by Denmark, Poland, the Czech Republic, Austria, Switzerland, France, Luxembourg, Belgium, and the Netherlands to the west. Its capital and most populous city is Berlin and its main financial center is Frankfurt. The largest urban area is the Ruhr.
```



## Medium Articles
### Introduction
https://medium.com/@paolorechia/creating-my-first-ai-agent-with-vicuna-and-langchain-376ed77160e3
### Q/A with Sentence Transformer + Vicuna
https://medium.com/@paolorechia/building-a-question-answer-bot-with-langchain-vicuna-and-sentence-transformers-b7f80428eadc

## Example run
https://gist.github.com/paolorechia/0b8b5e08b38040e7ec10eef237caf3a5


## Acknowledgements

* The quantized models are a direct copy of this repository: https://github.com/qwopqwop200/GPTQ-for-LLaMa
* The inference code is slightly modified version of FastChat: https://github.com/lm-sys/FastChat
* All model creators / community that are training and sharing models
