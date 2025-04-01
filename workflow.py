from openai import OpenAI
import os
import markdown
import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict, List, Union
import time


#################        models           ##################################

def deepseek_r1(input_text):
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    reasoning_content = ""
    answer_content = ""
    is_answering = False
    
    # Create chat completion request
    completion = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "user", "content": input_text}
        ],
        stream=True
    )
    
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    
    # Process the stream
    for chunk in completion:
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
            continue
        
        delta = chunk.choices[0].delta
        
        # Print reasoning content (if exists)
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        
        # Print answer content (if exists)
        elif delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            print(delta.content, end='', flush=True)
            answer_content += delta.content
    
    return answer_content

def deepseek_v3(input_text):
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    reasoning_content = ""
    answer_content = ""
    is_answering = False
    
    # Create chat completion request
    completion = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {"role": "user", "content": input_text}
        ],
        stream=True
    )
    
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    
    # Process the stream
    for chunk in completion:
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
            continue
        
        delta = chunk.choices[0].delta
        
        # Print reasoning content (if exists)
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        
        # Print answer content (if exists)
        elif delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            print(delta.content, end='', flush=True)
            answer_content += delta.content
    
    return answer_content


def Qwen_max(input_text):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    completion = client.chat.completions.create(
        model="qwen-max",
        messages=[
            {"role": "user", "content": input_text}
        ],
        stream=True
    )

    for chunk in completion:
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
            continue
        
        delta = chunk.choices[0].delta
        
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        
        # Print answer content (if exists)
        elif delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            print(delta.content, end='', flush=True)
            answer_content += delta.content
    
    return answer_content
#example
#test1 = deepseek_r1("9.9和9.11谁大")


##########################      nodes         ###########################################

def read_md(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        md_text = file.read()
        html_content = markdown.markdown(md_text)
    return {'grammer_content':html_content}
#html_output = read_md('D:/code/PPTagent/test3/1/111.md')
#print(html_output)

def arxiv_png_crawler(url: str, max_retries: int =3, timeout: int =15,retry_delay: int =2) -> Dict[str, List[str]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml'
    }
    
    if not url.startswith(('http://', 'https://')):
        return {"error": "Invalid URL format"}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', {'src': lambda x: x and x.lower().endswith('.png')})
            
            base_url = url if url.endswith('/') else url + '/'
            png_urls = [urljoin(base_url, img['src']) for img in img_tags]
            
            return {"png_images": list(dict.fromkeys(png_urls))}
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return {"error": f"Failed after {max_retries} attempts: {str(e)}"}
            time.sleep(retry_delay) 
            
    return {"error": "Unknown error"}

#result = arxiv_png_crawler('https://arxiv.org/html/2406.08232v1', timeout=15)
#print(result)


def text_crawler(url: str,max_retries: int = 3,timeout: int = 10,retry_delay: int = 2) -> Dict[str, Union[str, None]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml'
    }
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"第 {attempt + 1} 次尝试...")
                
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'footer', 'head', 'meta', 'iframe', 'noscript']):
                element.decompose()
            
            text = soup.get_text(separator='\n', strip=True)
            return {'text': text}

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            print(f"请求失败（尝试 {attempt + 1}/{max_retries}）: {last_error}")
            
            if attempt == max_retries - 1:
                return {'error': f"重试{max_retries}次后失败: {last_error}"}
                
            time.sleep(retry_delay)  
    
    return {'error': '未知错误'}
#result = text_crawler('https://arxiv.org/html/2406.08232v1')
#print(result)

def summary(messages: dict)->dict:
    prompt = f"""
    你是一个论文总结器。你的任务是将它总结, 输出一个 markdown文件. 这个文件必须是英文,包括题目, 作者, 单位等重要基本信息,对每个部分进行简单概括，每个板块保留约200词的文本.
    为了更好的总结论文，需要知道总结论文并生成markdown文件时应该注意的原则。这些原则是什么呢？
    在总结一篇论文并生成英文 Markdown 文件时，需遵循以下原则以确保内容的专业性和有效性：
    总结原则
    1.**准确性优先**：确保所有信息（标题、作者、单位、方法、结论等）与原文完全一致，避免主观臆断或模糊表述。关键术语、数据和公式需与原文核对，不可随意简化或修改。
    2.**结构清晰**：按论文逻辑分段（如摘要、引言、方法、结果、讨论等），每部分独立成块，用 Markdown 标题（## 或 ###）标注。每部分内容控制在 200 词左右，提炼核心观点，删除冗余细节（如冗长的实验步骤、重复论证）。
    3.**保持客观中立**：避免个人评价（如“这项研究非常创新”），仅陈述作者观点和发现。区分原文的“事实”与“推测”（如明确标注“作者提出假设...”或“研究结果表明...”）。
    4.**学术规范**：标注原文引用格式（如(Smith et al., 2023)），若引用原文图表需注明编号（Figure 1）。避免直接复制长段落，需用自己的语言概括，同时不遗漏关键贡献。
    5.**可读性与简洁性**：使用学术英语，但避免复杂句式。可用短句和列表（如 - 或 *）分点说明核心贡献或方法步骤。技术术语首次出现时给出简短定义（如“BERT (Bidirectional Encoder Representations from Transformers)”）。
    6.**格式规范**：Markdown 文件需包含必要元信息（标题、作者、单位、原文链接或 DOI）。代码块或公式用反引号（`）或 LaTeX 语法（$$E=mc^2$$）清晰标注。
    7.**版权与伦理**：若论文未开放获取，避免总结敏感数据或核心算法细节。在文件末尾注明原文来源（如“Source: 论文标题”）。
    {messages['text']}这是一篇论文,根据上述原则, 请将它总结, 输出一个 markdown 文件. 这个文件必须是英文, 包括题目, 作者, 单位等重要基本信息,对每个部分进行简单概括，每个板块保留约200词的文本
    """
    output = deepseek_v3(prompt)
    return {'summary':output}

def image_caption(messages:dict)->dict:
    prompt=f"""
    你是一个论文图片解析器，负责专门从论文中读取图像元数据并生成结构化标记
    当我提供给你图片URL和论文文本时,你该怎么做呢?
    当用户提供图片URL和关联文本标识时，执行以下操作：- 解析文本标识对应的上下文段落- 识别插图的学术属性- 提取以下6个核心要素：
    a. 图片标题（精确匹配原文）
    b. 图片URL（原始链接）
    c. 技术解释（说明图像展示的核心科学内容）
    d. 原文定位（章节编号+前后2句关键上下文）
    e. 上下文概括（50字内说明插图目的）
    f. 原始文件名字（从URL解析，保留扩展名）
    2. 输出要求：- 使用Markdown表格格式- 英语- 技术解释需包含：研究对象、可视化维度、关键特征标注- 按原文出现顺序排列
    {messages['png_images']}这是文章的插图的url, 请结合{messages['text']}文章中对这些图片的引用位置的上下文, 和上述你应实现的操作, 给这些图片打标签
    , 包括图片的标题, 图片对应的url，详细的图片解释,在原文中出现的位置, 图片在原文出现的上下文的概括, 以及图片的文件名称,名称使用图片上传时候的名称. 输出一个 markdown 文件
    """
    output = deepseek_v3(prompt)
    return {'image_caption':output}

def code_gen(messages: dict)->dict:
    prompt= f"""
    你是一个markdown文件生成器，用于生成可以通过slidev执行的markdown文件
    {messages['grammer_content']}这是 slidev 的一个示例文件. 请你根据这个文件所描述的语法, 根据文本内容{messages['text']}和图片描述内容{messages['image_caption']},生成一个用于生成slidev的markdown文件.
    总体要求: 1. 第一页是标题和作者页. 2. 最后一页是总结页. 3. 总共不超过8页 4.用英语 5.图片和文字不得超出画面，长宽最多占页面长宽的的3/4 6.不改变原始图片长宽比 7.第一页应该是整篇文章的标题，而不是单独的一章图片
    每个页面需要满足以下11个要求: 
    1. 所有文字和图片应该在页面内 1. 同一列元素不能过多, 如果元素过多需要拆成多列, 防止超出页面边框, 同一列文字必须小于8行.
    2. 每个页面元素不能太少, 如果太少, 可以适当扩充内容. 如果某一列只有文字没有图片, 文字不能少于3行.
    3. 如果某几列只有图片而没有其他文字, 那么图片应该居中显示.
    4. 如果你要将每个页面分成三列, layout 不是 three-col, 因为 slidev 不支持这种布局, 你需要使用 default layout 配合 Tailwind CSS 的 grid 系统来实现三列布局.
    5. 考虑图片的宽高比, 如果宽高比大于2:1, 那么在多列布局下, 不能出现在单独的一列, 而是横跨多列. 否则, 图片应该出现在没有文字单独一列.
    6. 如果某一列同时有文字和图片, 那么图片的高度(max-h)和文字行数(x)满足 max-h + 5x = 65. 如果图片横跨多列, 按文字行数最多的那一列计算.例如 x=5, 高度设置为 max-h-40, 不是 max-h-[40vh]
    7.对于含有图片的页面的文字，需要检查图片是否在三列布局中横跨多列。 若横跨多列则图片在页面上部分而文字在下部分，且文字也横跨多列。 若图片只在一列内，则文字只能存在于剩下两列
    8.有图片的页面必须包含相应的文字说明 
    9. 每页ppt只能有一个小标题
    10.对于反复出现的重要概念在正文中可以加上<strong></strong>粗体强调
    11.将图片和标题用 <figure> 和 <figcaption> 包裹起来而不是<p>
    12.所有内容应该与页面的边框有一定间距，例如页面尺寸为200*100，那么所有文本和图片所在的区域大小为150*75，存在内容部分和整个页面的长宽比为3：4
    插入的图片需要满足以下9个要求: 
    1. 每张图片都有标题, 标题在图片正下方紧贴显示.
    2. 图片的插入不要插在 frontmatter 中, 也不要使用 markdown 默认的插入, 必须是 <img src= 这种格式, 符合 Vue 语法. 图片路径使用相应的url.
    3. 图片的大小需要符合页面尺寸, 不能超出边框.
    4. 图片插入的页面位置, 需要符合原文的上下文语境.
    5. 图片插入不使用 ZoomImg, 而是普通的 img.
    6. 检查总图片的数量是否正确, 不要插入任何没有出现的图片或图标或GIF.
    7. 所有图片都是 PNG 格式.
    8. 不能改变图片的原始长宽比例. 不能使用 class="max-h-[40vh] w-full mt-4" 这种写法, 因为比例会改变
    9.在多列布局中，若图片存在于单独的一列并且长宽比小于1：1，可以等比例放大或缩小图片，使其在不超出ppt页面的情况下，宽度尽量占满该列
    10.图片原始的长宽比无论如何不可以改变
    """
    output = deepseek_r1(prompt)
    return {'code_gen':output}

def check(messages: dict)->dict:
    prompt = f"""
    你是一个代码检查点，负责检查传入的代码是否符合下述规则。
    {messages['grammer_content']}这是 slidev 的一个示例文件. 请你检查 {messages['code_gen']}这个文件是否符合上述语法, 且满足如下要求. 如果满足, 直接输出 "yes", 否则输出需要改正的地方.
    总体要求: 1. 第一页是标题和作者页. 2. 最后一页是总结页. 3. 总共不超过8页 4.用英语 5.图片和文字不得超出画面，长宽最多占页面长宽的的3/4 6.不改变原始图片长宽比 7.第一页应该是整篇文章的标题，而不是单独的一章图片
    每个页面需要满足以下11个要求: 
    1. 所有文字和图片应该在页面内 1. 同一列元素不能过多, 如果元素过多需要拆成多列, 防止超出页面边框, 同一列文字必须小于8行.
    2. 每个页面元素不能太少, 如果太少, 可以适当扩充内容. 如果某一列只有文字没有图片, 文字不能少于3行.
    3. 如果某几列只有图片而没有其他文字, 那么图片应该居中显示.
    4. 如果你要将每个页面分成三列, layout 不是 three-col, 因为 slidev 不支持这种布局, 你需要使用 default layout 配合 Tailwind CSS 的 grid 系统来实现三列布局.
    5. 考虑图片的宽高比, 如果宽高比大于2:1, 那么在多列布局下, 不能出现在单独的一列, 而是横跨多列. 否则, 图片应该出现在没有文字单独一列.
    6. 如果某一列同时有文字和图片, 那么图片的高度(max-h)和文字行数(x)满足 max-h + 5x = 65. 如果图片横跨多列, 按文字行数最多的那一列计算.例如 x=5, 高度设置为 max-h-40, 不是 max-h-[40vh]
    7.对于含有图片的页面的文字，需要检查图片是否在三列布局中横跨多列。 若横跨多列则图片在页面上部分而文字在下部分，且文字也横跨多列。 若图片只在一列内，则文字只能存在于剩下两列
    8.有图片的页面必须包含相应的文字说明 
    9. 每页ppt只能有一个小标题
    10.对于反复出现的重要概念在正文中可以加上<strong></strong>粗体强调
    11.将图片和标题用 <figure> 和 <figcaption> 包裹起来而不是<p>
    12.所有内容应该与页面的边框有一定间距，例如页面尺寸为200*100，那么所有文本和图片所在的区域大小为150*75，存在内容部分和整个页面的长宽比为3：4
    插入的图片需要满足以下9个要求: 
    1. 每张图片都有标题, 标题在图片正下方紧贴显示.
    2. 图片的插入不要插在 frontmatter 中, 也不要使用 markdown 默认的插入, 必须是 <img src= 这种格式, 符合 Vue 语法. 图片路径使用相应的url.
    3. 图片的大小需要符合页面尺寸, 不能超出边框.
    4. 图片插入的页面位置, 需要符合原文的上下文语境.
    5. 图片插入不使用 ZoomImg, 而是普通的 img.
    6. 检查总图片的数量是否正确, 不要插入任何没有出现的图片或图标或GIF.
    7. 所有图片都是 PNG 格式.
    8. 不能改变图片的原始长宽比例. 不能使用 class="max-h-[40vh] w-full mt-4" 这种写法, 因为比例会改变
    9.在多列布局中，若图片存在于单独的一列并且长宽比小于1：1，可以等比例放大或缩小图片，使其在不超出ppt页面的情况下，宽度尽量占满该列
    10.图片原始的长宽比无论如何不可以改变
    """
    output = deepseek_r1(prompt)
    return {'check':output}

def code_gen2(messages:dict)->dict:
    prompt = f"""
    你是一个markdown文件生成器，用于生成可以通过slidev执行的markdown文件
    {messages['grammer_content']}这是 slidev 的一个语法示例文件. 请你学习这个文件的语法和排版，根据f{messages['check']}的修改意见, 修改 {messages['code_gen']}, 输出一个 markdown 文件.
    """
    output = deepseek_r1(prompt)
    return {'code_gen':output}

def ending(messages: dict):
    try:
        content = messages.get('code_gen', '')
        if not content:
            raise ValueError("输入字典中缺少 'code_gen' 键")
            
        markdown_content = content.split('```markdown\n')[1].split('\n```')[0]
        
        with open('D:/code/PPTagent/test3/1/slides.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        return {"status": "success", "path": "D:/code/PPTagent/test3/1/slides.md"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    messages = {}

    arxiv_url = 'https://arxiv.org/html/2503.21801v1'
    grammar_md = 'D:/code/PPTagent/test3/1/111.md'

    messages.update(read_md(grammar_md))  # key = grammer_content
    messages.update(arxiv_png_crawler(arxiv_url))  # key =  png_images
    messages.update(text_crawler(arxiv_url))  # key = text
    #print(json.dumps(messages,indent =4)
    print('The pngs and text are successfully crawled')

    ###############   summary  ##############
    print('\n' + '*'*20 + 'Summary' + '*'*20 + '\n')
    messages.update(summary(messages))  # key = summary
    #print(messages['summary'])

    ##############   image_caption  ##############
    print('\n' + '*'*20 + 'image_caption' + '*'*20 + '\n')
    messages.update(image_caption(messages)) #key = image_caption
    #print(json.dumps(messages['image_caption']))

    ##############    code_gen    ################
    print('\n' + '*'*20 + 'code_gen' + '*'*20 + '\n')
    messages.update(code_gen(messages))  #key = code_gen

    ##############   check   #####################
    print('\n' + '*'*20 + 'check' + '*'*20 + '\n')    
    messages.update(check(messages))   #key = check

    if messages['check'] != 'yes':
        messages.update(code_gen2(messages))
    
    ending(messages)
    



if __name__ == '__main__':
    main()