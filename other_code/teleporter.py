from bs4 import BeautifulSoup

class Teleporter(BeautifulSoup):
    def __init__(self,html):
        super().__init__(html,"html.parser")

        self.teleporter = self.CreateTeleporter()

    def CreateTeleporter(self):
        html = ""
        link_template = "\n<a class='nav-link' href='#{id}'>{content}</a>\n"
        sub_navigation_template = "\n<nav class='nav nav-pills flex-column ml-3 my-1'>\n{content}\n</nav>\n"
        sections = self.find_all("div",class_="section")
        for section in sections:
            h2 = section.findChild("h2")
            html += link_template.format(id=h2.get("id"),content=h2.text.strip()) 
            sub_navigation = ""
            h3_s = section.findChildren("h3")
            for h3 in h3_s:
                sub_navigation+=link_template.format(id=h3.get("id"),content=h3.text.strip())
            
            html+=sub_navigation_template.format(content=sub_navigation)

        return html