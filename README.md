

## 环境安装：

- **pdfminer.six** 指定版本
- **interval = 1.0.0**
- **python >= 3.10**
- **pytorch**

```bash
conda create -n CED python=3.10
conda activate CED
pip install interval
```

pdfminer.six安装：

```bash
pip install git+https://github.com/PUBGprofessor/pdfminer.six.git
```

## RUN：

### 1.基于规则的目录提取：

```bash
python .\main.py -d 281834793.pdf -o output\281834793.txt
```

output\281834793.txt的每行内容为：

"degree_rules, fontsize, fontname,linewidth,left(左端),center(中点),width(字块所占宽度),height(字块所占高度), pageid, 文本" 

### 2. 提取PDF特征到txt，默认目录设为0：

```bash
python .\main.py -d 281834793.pdf -o output\281834793.txt --x
```

output\281834793.txt的每行内容为：

"0, fontsize, fontname,linewidth,left(左端),center(中点),width(字块所占宽度),height(字块所占高度), pageid, 文本" 

### 3. 自动提取pdf自带目录：

```
python .\mulu.py -p 281834793.pdf -t output\281834793.txt -o output\281834793_self.txt
```

其中，281834793.pdf为原pdf文件， output\281834793.txt为1或2步得到的txt特征文件，output\281834793_self.txt为pdf自带的正确目录，格式仍为：

"degree_self, fontsize, fontname,linewidth,left(左端),center(中点),width(字块所占宽度),height(字块所占高度), pageid, 文本" 

### 4. 将上面得到的特征txt转换为目录txt：

```
python .\txt_convert.py -i output\281834793.txt -o output\281834793_.txt
```

output\281834793_.txt内容为：

> 一、2023 年年度主要财务数据和指标 **\**1
> 二、业绩泄漏原因分析 **\**1
> (一）公司出现业绩提前泄漏 **2

### 5. 多进程并行处理大量文件：

```bash
python cowokers.py
```

