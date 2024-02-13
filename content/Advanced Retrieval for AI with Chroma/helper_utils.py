import chromadb
import re
import numpy as np

from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from pypdf import PdfReader
from tqdm import tqdm


def _read_pdf(filename):
    """
    读取PDF文件。
    Read the text content from the given PDF file.

    Args:
    filename (str): The path to the PDF file.

    Returns:
    list: A list of text content from each page of the PDF file.
    """
    reader = PdfReader(filename)
    
    # Extract text from each page and remove leading/trailing whitespaces
    pdf_texts = [p.extract_text().strip() for p in reader.pages]

    # Filter the empty strings
    pdf_texts = [text for text in pdf_texts if text]
    return pdf_texts


def _chunk_texts(texts, langcode="zh"):
    """
    将输入文本分块。
    Splits the input texts into chunks for processing.

    Args:
        texts (list): List of input texts to be chunked. 输入文本。
        langcode (str, optional): Language code of the input texts. Defaults to "zh".
        语言选项: 中文: zh; 英文: en

    Returns:
        list: List of chunked texts. 分块后的文本。
    """

    assert langcode in ['zh', 'en'], "langcode must be 'zh' or 'en'"

    # 1.用\n\n拼接所有文本；2.字符级分割，分割成多个块(chunk)；3. 对每一个块分割成token
    if langcode == 'zh':
        # 中文句子分割
        def chinese_sentence_segmentation(text):
            # 使用正则表达式匹配中文句子的分割符号，将中文分句
            sentences = re.split(r'[，。！？]', text)
            return [s.strip() for s in sentences if s.strip()]
        
        character_split_texts = []
        for text in texts:
            # 每个段落逐个分割句子
            character_split_texts += chinese_sentence_segmentation(text)
    else:
        # 英文句子分割
        character_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""], # 英文
            # separators=["\n\n", "\n", "。", "，", ""], # 中文
            chunk_size=1000,
            chunk_overlap=0
        )
        character_split_texts = character_splitter.split_text('\n\n'.join(texts))

    # Split each character-based chunk into tokens
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)

    token_split_texts = []
    if langcode == "zh":
        # 中文分句后不再进一步分割，保留完整语义信息，方便嵌入查询
        token_split_texts = character_split_texts
    else:
        # 英文分句后继续分割token（实际上这一步分割得很少）
        for text in character_split_texts:
            token_split_texts += token_splitter.split_text(text)

    return token_split_texts

def load_chroma(filename, collection_name, embedding_function, langcode='zh'):
    """
    加载PDF文件，分块，初始化chroma集合
    Load text from a PDF file, chunk it, create a collection, add the chunks, and return the collection.

    Args:
        filename (str): The name of the PDF file.
        collection_name (str): The name of the collection to be created.
        embedding_function (function): The embedding function to be used for the collection.
        langcode (str, optional): The language code. Defaults to 'zh'.

    Returns:
        chroma_collection: The created collection.
    """
    # Read the text from the PDF file
    texts = _read_pdf(filename)
    
    # Chunk the texts based on the language code
    chunks = _chunk_texts(texts, langcode)

    # Create a new ChromaDB client
    chroma_client = chromadb.Client()

    # Create a new collection with the specified name and embedding function
    chroma_collection = chroma_client.create_collection(name=collection_name, 
                                                        embedding_function=embedding_function)

    # Generate IDs for the chunks
    ids = [str(i) for i in range(len(chunks))]

    # Add the chunks to the collection
    chroma_collection.add(ids=ids, documents=chunks)

    return chroma_collection

def word_wrap(string, n_chars=72):
    """
    在指定字符数后的下一个空格处换行字符串.
    Wrap the string at the next space after a specified number of characters

    Args:
        string: The input string
        n_chars: The maximum number of characters before wrapping

    Returns:
        The wrapped string
    """
    if len(string) < n_chars:
        return string
    else:
        return string[:n_chars].rsplit(' ', 1)[0] + '\n' + word_wrap(string[len(string[:n_chars].rsplit(' ', 1)[0])+1:], n_chars)

   
def project_embeddings(embeddings, umap_transform):
    """
    用 UMAP 将高维的embeddings矩阵投影到2维，方便可视化。
    Project embeddings to a lower dimensional space using UMAP transformation.
    
    Args:
        embeddings (array-like): The original embeddings to be transformed.
        umap_transform (umap.UMAP): The UMAP transformation model.
    
    Returns:
        array-like: The UMAP-transformed embeddings.
    """

    umap_embeddings = np.empty((len(embeddings),2))
    for i, embedding in enumerate(tqdm(embeddings)): 
        umap_embeddings[i] = umap_transform.transform([embedding])
    return umap_embeddings