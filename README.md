# Chat with your Dataset

This project demonstrates a web-based application to query a dataset through natural language.

![Screenshot 2024-03-18 at 12 43 18 PM](https://github.com/asieduofeijnr/chatwithdataset/assets/114332208/168ada95-6279-4350-b183-423c5690b9df)


For this purpose, it uses:

- [Streamlit](https://streamlit.io/) to build a data science web app
- [Pandasai](https://pandas-ai.com/) to generate Pandas code from a query through [OpenAI GPT-3.5](https://platform.openai.com/docs/api-reference)

## Download dataset

Download the [dataset](https://github.com/Fraud-Detection-Handbook/simulated-data-transformed) into the `data` folder at the root of the project.

## Run the project

If you don't have a Python environment available, you can use the [conda package manager](https://docs.conda.io/projects/conda/en/latest/index.html) which comes with the [Anaconda distribution](https://www.anaconda.com/download) to manage a clean Python environment.

Create a new environment and activate it:

```sh
conda create -n streamlit-pandasai python=3.9
conda activate streamlit-pandasai
```

Install Python dependencies in the activate Python environment:

```sh
pip install -r requirements.txt
```

Create a [new API key](https://platform.openai.com/account/api-keys) and set it to the `OPENAI_API_KEY` environment variable beforehand.

![Screenshot 2024-03-18 at 12 49 46 PM](https://github.com/asieduofeijnr/chatwithdataset/assets/114332208/92695a29-4f85-4481-9c26-0bce45863bc2)



On Windows:

```bash
set OPENAI_API_KEY="sk-..."
```

On Unix:

```sh
export OPENAI_API_KEY="sk-..."
```

Run the Streamlit project:

```sh
streamlit run streamlit_app.py
```
