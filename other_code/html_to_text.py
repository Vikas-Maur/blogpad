from bs4 import BeautifulSoup

IMG_ATTRIBUTES = {
    "class":"img-fluid"
    ,"alt":""
}

VIDEO_ATTRIBUTES = {
    "class":"container-fluid"
    ,"title":"If the video does not load then please refresh/reload the page"
    ,"preload":"none"
    ,"controls":""
    ,"muted":""
}

class HTML_TO_Text(BeautifulSoup):
    def __init__(self,html):
        super().__init__(html,"html.parser")
        self.tag_blocks = []

        self.entries = {
            "title" : self.findChild("title").text.strip()
            ,"meta_desc" : self.findChild("meta", {"name": "description"}).get("content").strip()
            ,"language" : self.findChild("code")
        }
        if not self.entries["language"]:
            self.entries["language"] = "python"
        else:
            self.entries["language"] = self.entries["language"].get("language")


        self.ConvertToText()

    def InnerHTML(self,element):
        # text = ""
        # for t in element.contents:
        #     text+=str(t)
        # return text
        return element.decode_contents()

    def ConvertToText(self):
        sections = self.find_all("div",class_="section")
        text_records = []
        h1 = self.findChild("h1")
        if h1:
            text_records.append((h1.text.strip(),"h1"))
        for section in sections:
            child_elements = tuple(section.findChildren(recursive=False))
            for child in child_elements:
                name = child.name
                tabpanels = child.findChildren("div",role="tabpanel")

                if name not in ("img","video"):
                    if not child.text.strip():
                        continue

                if tabpanels: # means that code+tab is there
                    inner_html = self.ConvertTabSection(child)
                    name = "code+tab"
                elif name in ("h2","h3"):
                    inner_html = child.text.strip()
                elif name == "pre":
                    inner_html = self.InnerHTML(child.findChild("code"))
                    name = "code"
                elif name == "div":
                    inner_html = self.InnerHTML(child)
                    name = "normal"
                elif name=="img":
                    child = self.SetDefaultAttrs(child,IMG_ATTRIBUTES)
                    inner_html = str(child)
                elif name=="video":
                    child = self.SetDefaultAttrs(child,VIDEO_ATTRIBUTES)
                    inner_html = str(child)
                else:
                    inner_html = str(child)

                
                inner_html = inner_html.strip()
                text_records.append((inner_html,name))

        self.tag_blocks = tuple(text_records)

    def SetDefaultAttrs(self,child,attrs):
        for key,default_value in attrs.items():
            if not child.has_attr(key):
                child[key]=default_value
        return child

    def ConvertTabSection(self,child):
        codes = child.findChildren("code")
        tablinks = child.findChildren("a")
        inner_html = """"""
        for index,link in enumerate(tablinks):
            inner_html += self.InnerHTML(link)
            if index!=len(tablinks)-1:
                inner_html+=","
        inner_html+="\n"
        for index,code in enumerate(codes):
            inner_html += self.InnerHTML(code)
            if index!=len(tablinks)-1:
                inner_html += "\n---\n"
        return  inner_html

if __name__=="__main__":
    with open(r"C:\Users\vikas\OneDrive\Desktop\myFolder\myCODEnotein-2\src\python-modules.html") as f:
        html = f.read()
    test = HTML_TO_Text(html)
    print(test.tag_blocks[-1])


























