from tkinter import Button

COLORS = {
    'primary':'#0D6EFD',
    'secondary':'#6C757D',
    'success':'#198754',
    'danger':'#DC3545',
    'warning':'#FFC107',
    'info':'#0DCAF0',
    'light':'#F8F9FA',
    'dark':'#212529'
}

STYLES = {
    'notag':{}
    ,'normal':{'font':'consolas 18 bold','background':'white','foreground':'black'}
    ,'h1':{'font':'consolas 30 bold','foreground':COLORS['primary'],'background':'white'}
    ,'h2':{'font':'consolas 26 bold','foreground':COLORS['danger'],'background':'white'}
    ,'h3':{'font':'consolas 22 bold','foreground':COLORS['warning'],'background':'white'}
    ,'code':{'font':'consolas 18 bold','foreground':'white','background':'black'}
    ,'code+tab':{'font':'consolas 18 bold','foreground':'white','background':'black'}
    ,'img':{'background':COLORS['success'],'foreground':'white'}
    ,'video':{'background':COLORS['success'],'foreground':'white'}
}

MULTI_LINER_TAGS = ("code","code+tab")

TAG_TEMPLATES = {
    'normal':("<div id='{id}' class='normal'>","</div>","self.ConvertToNormalTag")

    ,'h1':("<h1 id='{id}'><span class='badge bg-primary'> </span> "
           ," <span class='badge bg-primary'> </span></h1>"
           ,"self.ConvertToNormalTag")

    ,'h2':("{section_end}<div class='section'><h2 id='{id}'><span class='badge bg-danger'> </span> "
           ,"</h2>","self.ConvertToH2")

    ,'h3':("<h3 id='{id}'><span class='badge bg-warning'> </span> ","</h3>","self.ConvertToNormalTag")

    ,'code':("<pre id='{id}'><code class='{language}' language='{language}'>","</code></pre>"
             ,"self.ConvertToCode")

    ,
    
    'code+tab':({
        'tag':"""
<div id='{id}'>
        <nav>
            <div class='nav nav-tabs' role='tablist'>
{tag_links}
            </div>
        </nav>
        <div class='tab-content'>
{tag_blocks}
        </div>
</div>
"""
        
        ,'link':"\n<a id='{id}' aria-controls='{target}' href='#{target}' class='nav-link {active}' aria-selected='{selected}' data-bs-toggle='tab' role='tab'>{content}</a>\n"
        
        ,'tag_block':"\n<div id='{id}' aria-labelledby='{link}' class='tab-pane fade show {active}' role='tabpanel'>\n<pre><code class='{language}' langauge='{language}'>{content}</code></pre>\n</div>\n"
    
    },"","self.ConvertToTabSection")
}

class HoverableButton(Button):
    def __init__(self,master,on_enter,**kwargs):
        super().__init__(master,**kwargs)

        self.on_leave = kwargs
        self.on_enter = on_enter

        self.bind('<Enter>',func=lambda e:self.config(**self.on_enter))
        self.bind('<Leave>',func=lambda e:self.config(**self.on_leave))