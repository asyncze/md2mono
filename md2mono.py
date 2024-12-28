
# md2mono
# static website/blog generator from Markdown files for easy hosting on Github pages or similar (host need build command feature)
# styling based on https://owickstrom.github.io/the-monospace-web

# py312 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
# deactivate

# python md2mono.py /website (both md2mono.py and website folder in root)

import os
import sys
import re
import shutil
import markdown
import sass
import traceback
from natsort import natsorted
from datetime import datetime
# syntax highlight
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

SOURCE_PATH                 = None
APP_THEME                   = "#000000"

# defaults
PAGE_TITLE                  = "asyncze"
POSTS_ON_INDEX              = False
STYLING                     = True
ALLOW_NO_STYLING            = False
DEFAULT_THEME               = ""                            # dark | ""
ALLOW_CHANGE_THEME          = False
CLEAN_INDEX                 = False                         # True | False
DEFAULT_FOOTER              = "simple"                      # full | simple | ""
NAV_POSITION                = "default"                     # left | default

# BODY_ALIGN                  = "left"                        # left | center [default:left]
FONT_SIZE                   = 14
MAX_WIDTH                   = 620

DIST_PATH                   = "/dist"
LOAD_FOLDER                 = False
LOAD_FOLDER_FLAGS           = False
AUTHOR                      = "@asyncze"
X_URL                       = "https://x.com/asyncze"
DESCRIPTION                 = "Self-funded software engineer"
GOOGLE_TAG                  = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-FPF1MCLY5P"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config','G-FPF1MCLY5P');</script>"""
APP_NAME                    = "Michael Sjöberg"
SOCIAL_IMAGE                = ""

# for listing all posts on index page
GLOBAL_POSTS = [] # [ { title, date, url } ]

def write_header(file, title="md2mono", root=0):
    file.write("<!DOCTYPE html>\n")
    file.write("""
    <!--
    #=-::::-+=+######%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    #==--:::-=+#######%%%%%%#%%%%%%%%%%%%%%%######%#%%%%%%%%%%%%##%%%%%%%%%%%%%#
    #=-:::::-==##****###%%%###%%%%%%%%%%%######***++**#%%###%%%%%%%%%%%%%%%#%%%%
    #=-:::::-==#########%%%%%%%%%#*#%%#####*=+++******+++*######%%%#**#%%%%%%%%%
    *=-:---=+==########*##########%###*++++=+*###*########**#####%%*++#%%%%##%%%
    *=++*****==#######%###**#########***-++*#######%##%%%%##=*######+*#%%%%%%%%%
    *=+****++-=###**#####*+++**#*****+==**+*%%##%%%%%%%%%%%##++##*#++*%%%%%%%%%%
    *=++-:-=*#####**###*#*##++*++=++===#*+*%###%%%%%%%%%%%%%##**####%%%%%%%%%%##
    *+=+***######****#***##**++=====-+##*+%###%%%%%%%@@@@@%%%%#*#####%%%%%%%%%##
    ******###*********#*****++=+=---=*##+####%#%@@@@@@@@@@@@%#%**####%##%%%%%%##
    *******##*##+++**+***+++**+==-.-+***####%@@@@@@@@@@@@@@@@@%#***#####%%%%%###
    *********###**+****++++++===-:==***##*#@@@@@@@@@@@@@@@@@@@@%*###########%%##
    ##******####**+++++==++==-::.-=**+***%@@@@@@@@@@@@@@@@@@@@@@%*###***++*#####
    #***++****++++====-------::::=++*++*%%%%##%%@@@@@@@@@@@@@@@%@***+=-:===+*++#
    #**+********++++=-=====-::..:=****+%%%%#++*#%@@@@@@@@@@@%@@%%++==-----=*####
    ###***+++++*++==-+++++=-----:=***+#%%%%%*+++*%%@@@@@%%##%%%%*+++++++++*#####
    ####*==-==+*+*+=+=**+#***+-=+=+##*#%@@@@%#++++##%%##*+**#%%#++++++****+++**#
    *##****+++-=++-==++**###******+#%##%%@@@@%%#*+++*+++**##%%#+++++=++++**#####
    +++++++===:-=-:*=**#######%%#*#*###%@@@@@@@@%#*+*##%%%%%%*=+++++=++*++++++*#
    +===-::--::-::==****##%%%%%%%%%%%%#%@@@@@@@@@@@%%@@@@%%%*===+=+++++=::..:=*#
    *+--====+=-:..-==+***++**#%@%%%%@%%%%@@@@@@@@@@@@@@%%%#+-===++==+**=::..:-+*
    *++++===---+****#*#**#######%%%#%%@@%%@@@@@@@@@@@@@%%#+-::-=+==++**=-:..::=*
    *+=++=--+-=+*#####%%#%##%#%##%@%#%%@%@@@@@@@@@@@%%%%#%****+=::-==**+=-==+++*
    ++==--=*#####%%#*#%%%%%%%%%%#%@@@@@%%%%%%@@@@@@@@%@%%%#***+:-=====:=---:::-+
    ++=-+##%%%%%%%%%%%##%%%%@%@%%%%%%%@@@@@@@@%%@%%@%%%@%###*=::--=-====-::...-+
    ++=*+*#%%%%###%%%%%@%%%@%@@%%%%@%#%%@%%@@@@@@%@@@%%%#%%#+:--:----=++=-....:=
    +==*#####%%%%@@@%%%@@@@@@@@@@%%%@%%%%%%%%@@@@@@%@%%%%%%#*+=:-::-:-=+=-:-===*
    ==+++*%%%%###%%%@@@@@@@@@@@@@@@@@%%#####%%%%%@@@@%%%%%%#***+---==-==+**++=**
    ==-*####%#%%%%%%%%%@@@@@@@@@@@@@@%%%%##%#%%%##%%%%%%%##%%##*++-=====+++++++*
    =-**########@%%%%@%@@%@@@@@@@@@@%@@@%#%%%%%%%%#%%#%%%%*%%%**#*+:--==+++=++++
    ==+#########%%%%%@@%%@@@@@@@@@@@@@@@%%%%%@@%%%%%%%%%%#**%%%#***==-=+++++****
    -=+*#%#####%%%%%@%@@@@@@@@@@@%@@@@@@%%@@@@%%%@%%%%%%%%%##%%##**+*--++++****+
    -=++**#####%#%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@%%%@%%@@@%%%##%%%##*+*=======++**
    :-***#%%%%%%%###%%%@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@%@%%%#%%%%%###*#====-=+===
    +=+*#####%%%@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@%%%%%%##**=--=====+*
    =*#%%%%@@@@@%%%@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@%%@@@%@%%%%@%%##**--===++++
    #*%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@%github.com/asyncze
    -->
    """.replace("    ", ""))
    file.write("""<html lang="en">""")
    file.write("<head>")
    # favicon
    file.write("<link rel='icon' href='/favicon.png'>")
    # title
    file.write(f"<title>{title}</title>")
    # meta
    file.write("<meta charset='utf-8'>")
    file.write("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    file.write(f"""<meta name='author' content='{AUTHOR}'>""")
    file.write(f"""<meta name='description' content="{DESCRIPTION}">""")
    file.write(f"<meta name='theme-color' content='{APP_THEME}'>")
    file.write(f"<meta name='application-name' content='{APP_NAME}'>")
    file.write(f"""<meta name='apple-mobile-web-app-title' content="{title}">""")
    file.write("<meta name='apple-mobile-web-app-capable' content='yes'>")
    file.write("<meta name='mobile-web-app-capable' content='yes'>")
    file.write(f"<meta name='apple-mobile-web-app-status-bar-style' content='{APP_THEME}'>")
    # social
    file.write("<meta property='og:type' content='website'>")
    file.write(f"""<meta property='og:title' content="{title}">""")
    file.write(f"""<meta property='og:description' content="{DESCRIPTION}">""")
    file.write(f"<meta property='og:image' content='/{SOCIAL_IMAGE}'>")
    # twitter
    file.write("<meta name='twitter:card' content='summary'>")
    file.write(f"""<meta name='twitter:title' content="{title}">""")
    file.write(f"""<meta name='twitter:description' content="{DESCRIPTION}">""")
    file.write(f"<meta name='twitter:image' content='/{SOCIAL_IMAGE}'>")
    # css
    with open("style.css", "r") as css_file:
        content = css_file.read()
        file.write("<style>")
        file.write(content)
        file.write("</style>")

    # import fontawesome
    file.write("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css' integrity='sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==' crossorigin='anonymous' referrerpolicy='no-referrer'>")
    file.write("</head>")
    # -------------------------------------------
    file.write("<body>")
    # google tag
    file.write(GOOGLE_TAG)
    # page
    file.write("<div class='page'>")
    # nav
    if os.path.exists(f"{SOURCE_PATH}/nav.md"):
        nav_file = open(f"{SOURCE_PATH}/nav.md", "r")
        nav_content = nav_file.read()
        nav_file.close()
        if len(nav_content) != 0:
            file.write("<div class='nav no-print'>")
            file.write(markdown.markdown(nav_content))
            # theme toggle
            if ALLOW_CHANGE_THEME:
                file.write("""
                    <input type="checkbox" class="sr-only" id="theme">
                    <label for="theme" class="toggle">
                        <i class='fa-solid fa-adjust' style='font-size:120%'></i>
                    </label>
                """)
            file.write("</div>")
        elif "index.html" not in file.name:
            file.write("<div class='nav no-print'>")
            # render home link on pages if nav is empty
            file.write("<p><a href='/'>Home</a></p>")
            # theme toggle
            if ALLOW_CHANGE_THEME:
                file.write("""
                    <input type="checkbox" class="sr-only" id="theme">
                    <label for="theme" class="toggle">
                        <i class='fa-solid fa-adjust' style='font-size:120%'></i>
                    </label>
                """)
            file.write("</div>")
        else:
            # empty nav for aligned padding across pages
            file.write("<div class='nav no-print'><p></p></div>")

def write_footer(file):
    # credits
    if file.name.split("/")[-1] == "index.html":
        file.write("""<div id="footer" class="no-print">""")
        file.write(f"""<p><i class="fa-regular fa-copyright"></i> { datetime.now().year } <a href="{X_URL}">{AUTHOR}</p>""")
        file.write("</div>")
    
    file.write("</div>") # ./page
    # end of file
    file.write("</body>")
    file.write("</html>")

# helpers
def sort_by_date_and_title(item): return (item["date"], item["title"])

def generate_checklist_from_list(file_content):
    checklist = False
    
    result = []
    for line in file_content.split("\n"):
        if line == "<!-- checklist -->": checklist = True

        if "<ul>" in line:
            result.append("<ul class='checklist'>")
        elif checklist == True and "[X]" in line:
            result.append(line.replace("[X]", "<span style='color:#31D06A'><i class='fa-solid fa-check'></i></span>"))
        elif checklist == True and "[ ]" in line:
            result.append(line.replace("[ ]", "<span class='text-muted'>–</span>"))
        elif checklist == True and "</ul>" in line:
            checklist = False
            result.append(line)
        else:
            result.append(line)

    return "".join(result)

def generate_and_inject_index(file_content):
    # generate anchors
    file_content = re.sub(r"## (.*)", r"## \1 <a name='\1'></a> <a class='anchor' href='#\1'>#</a>", file_content)
    # find anchors and generate index
    index = []
    for line in file_content.split("\n"):
        if line.startswith("## "):
            anchor = line.split("## ")[1].split("<a")[0].strip()
            index.append(f"- [{anchor}](#{anchor})")
        if line.startswith("### "):
            anchor = line.split("### ")[1].split("<a")[0].strip()
            index.append(f"    - [{anchor}](#{anchor})")
    if len(index) > 0:
        # inject index as list just before first line starting with ##
        file_content = re.sub(r"## (.*)", f"\n".join([f"{item}" for item in index]) + "\n --- \n" + r"\n## \1", file_content, count=1)
    return file_content

def generate_post_index(dir_page, FLAG_SORT, FLAG_COL, posts_lst=[], posts_dict={}):
    sorted_posts_lst = sorted(posts_lst, key=sort_by_date_and_title, reverse=True)
    # write posts_lst (list by date)
    dir_page.write("<dl>")
    for post in sorted_posts_lst:
        # dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a> <span class='' style='float:right;'><em>{datetime.date(post['date']).strftime('%B %d, %Y') if post['date'] else ''}</em></span></li>")
        dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
    dir_page.write("</dl>")
    # create list with categories for ordering
    category_list = sorted(posts_dict.keys())
    # write posts in posts_dict (list by category and subcategory)
    for category in category_list:
        # write category
        dir_page.write(f"<h2 id='{category}'>{category.title()}</h2>")
        for subcategory in posts_dict[category]:
            sorted_posts_dict = natsorted(posts_dict[category][subcategory], key=lambda item: item["title"])
            # subcategory name
            if subcategory != "_root":
                dir_page.write(f"<p id='{category.lower()}-{subcategory.replace(' ', '-').lower()}'>{subcategory.replace('-', ' ')}</p>")
            # mulitple columns
            if FLAG_COL: dir_page.write(f"<dl class='columns' style='column-count:{FLAG_COL};'>")
            else: dir_page.write("<dl>")
            for post in sorted_posts_dict:
                # if date is current or last month
                if post['date'] and (post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1):
                    dir_page.write(f"<li><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></li>")
                else:    
                    dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
            dir_page.write("</dl>")

def replace_hr_with_border(file_content, toc=False):
    file_content = re.sub(r"<hr />\n<ul>", f"<p>In this post:</p>" + r"<ul class='toc'>\n" if toc else "", file_content)
    file_content = re.sub(r"</ul>\n<hr />", r"</ul><hr>", file_content)
    return file_content

def syntax_highlight(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    code_blocks = soup.find_all("code")
    if code_blocks:
        for code_block in code_blocks:
            try:
                code_content = code_block.get_text()
                code_language = code_block.get('class')[0].split("-")[1]
                lexer = get_lexer_by_name(code_language, stripall=True)
                formatter = HtmlFormatter(linenos=False, cssclass="highlight")
                highlighted_code = highlight(code_content, lexer, formatter)
                code_block.parent.unwrap()
                code_block.replace_with(BeautifulSoup(highlighted_code, "html.parser"))
            except:
                pass
        html_content = str(soup)
    return html_content

def parse_flags(line):
    FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
    if line.startswith("-* "):
        flags_raw = line[3:].split(";")
        for flag in flags_raw:
            key, value = flag.split("=")
            if key == "toc": FLAG_TOC = bool(value)
            if key == "time": FLAG_TIME = bool(value)
            if key == "col": FLAG_COL = int(value)
            if key == "sort": FLAG_SORT = "date" if value == "date" else "name"
            if key == "desc": FLAG_DESC = str(value)
    return FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC

def main_driver():
    # create dist folder
    # if os.path.isdir(DIST_PATH): shutil.rmtree(DIST_PATH)
    os.mkdir(DIST_PATH)
    # copy source __static folder to dist (images etc)
    if os.path.exists(f"{SOURCE_PATH}/__static"):
        os.system(f"cp -r {SOURCE_PATH}/__static {DIST_PATH}")
    # copy other stuff in source folder
    for file in os.listdir(SOURCE_PATH):
        if not file.startswith(".") and not file == "nav.md" and not os.path.isdir(f"{SOURCE_PATH}/{file}"):
            os.system(f"cp {SOURCE_PATH}/{file} {DIST_PATH}/{file}")
    # copy load folders into source
    if LOAD_FOLDER != False:
        os.system(f"rsync -av --progress {LOAD_FOLDER} {SOURCE_PATH} --exclude .git --exclude='_*'")
        # create file in source folder with flags for loaded folder
        with open(f"{SOURCE_PATH}/{LOAD_FOLDER.split('/')[-1]}/__flags", "w+") as file: file.write(LOAD_FOLDER_FLAGS)
    # create list page for each folder in root dir
    for dir_ in os.listdir(SOURCE_PATH):
        if "." not in dir_ and dir_ != "pages" and not dir_.startswith("__"):
            FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
            # check if __flags file in dir_
            if os.path.exists(os.path.join(f"{SOURCE_PATH}/{dir_}", "__flags")):
                flag_content = open(f"{SOURCE_PATH}/{dir_}/__flags").read()
                # parse flags
                FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = parse_flags(flag_content)
            # create page for folder
            with open(f"{DIST_PATH}/{dir_.lower()}.html", "w+") as dir_page:
                write_header(dir_page, title=dir_.title())
                # TODO: refactor this to single data structure and use flags to set ordering? (by date, category, etc)
                posts_lst = [] # [ { title, date, url } ]
                posts_dict = {} # { category: { subcategory: [ { title, date, url } ] } }
                # for each md file in dir_, create html page and append to posts_lst or posts_dict
                for root, dirs, posts in os.walk(f"{SOURCE_PATH}/{dir_}"):
                    root = root.replace(f"{SOURCE_PATH}/", "")
                    if ".git" not in root and "/_" not in root: os.mkdir(f"{DIST_PATH}/{root.lower()}")
                    for post in posts if ".git" not in root and "/_" not in root else []:
                        try:
                            if post != "__flags" and post != "README.md" and not post.startswith("_") and post.split(".")[1] in { "md" }:
                                post_file = open(f"{SOURCE_PATH}/{root}/{post}")
                                post_name = post.split(".")[0]
                                post_format = post.split(".")[1]
                                category, subcategory = None, None
                                date = False
                                # title from file name
                                post_title = post_name.replace("-", " ")
                                post_content = post_file.read()
                                # TODO: refactor this as helper function?
                                # create page
                                with open(f"{DIST_PATH}/{root}/{post_name.replace('#', '')}.html", "w+") as tmp_file:
                                    # title
                                    try: post_title = post_content.split("\n")[0].split("# ")[1]
                                    except: pass
                                    # date
                                    if not date:
                                        try: date = post_content.split("\n")[2].split("<mark>")[1].split("</mark>")[0]
                                        except:
                                            try: date = post_content.split("\n")[2].split("*")[1]
                                            except: pass
                                    # check if date is older than 2 years
                                    if date:
                                        try: date_is_outdated = True if datetime.strptime(date, "%B %d, %Y").year + 2 < datetime.now().year else False
                                        except: date_is_outdated = False
                                    # categories
                                    try: category, subcategory = root.split("/")[1], root.split("/")[2]
                                    except:
                                        try: category = root.split("/")[1]
                                        except: pass
                                    # category and subcategory
                                    if category and subcategory:
                                        try:
                                            if type(date) == type(""): date = datetime.strptime(date, "%B %Y")
                                        except: date = False
                                        if not category in posts_dict: posts_dict[category] = {}
                                        if not subcategory in posts_dict[category]: posts_dict[category][subcategory] = []
                                        # append
                                        posts_dict[category][subcategory].append({ "title": post_title, "date": date, "url": f"{root.lower()}/{post_name.lower().replace('#', '')}" })
                                    # category
                                    elif category:
                                        try:
                                            if type(date) == type(""): date = datetime.strptime(date, "%B %Y")
                                        except:
                                            try:
                                                date = datetime.strptime(date, "%B %d, %Y")
                                            except:
                                                date = False
                                        if not category in posts_dict: posts_dict[category] = { "_root": [] }
                                        # append
                                        posts_dict[category]["_root"].append({ "title": post_title, "date": date, "url": f"{root.lower()}/{post_name.lower().replace('#', '')}" })
                                    else:
                                        try:
                                            if type(date) == type(""): date = datetime.strptime(date, "%B %d, %Y")
                                        except: date = False
                                        # append to posts_lst
                                        posts_lst.append({ "title": post_title, "date": date, "url": f"{root.lower()}/{post_name.lower().replace('#', '')}" })
                                    GLOBAL_POSTS.append({ "title": post_title, "date": date, "url": f"{root.lower()}/{post_name.lower().replace('#', '')}" })
                                    # generate anchors and inject index
                                    post_content = generate_and_inject_index(post_content)
                                    # write
                                    write_header(tmp_file, title=post_title)
                                    # write outdated notice
                                    if date_is_outdated: tmp_file.write(f"<p class='text-center' style='margin-top:0;'><mark>This post is more than two years old and could be outdated</mark></p>")
                                    html_content = markdown.markdown(post_content, extensions=["fenced_code", "tables"])
                                    # replace hr with border (for table of contents)
                                    html_content = replace_hr_with_border(html_content, toc=True)
                                    # syntax highlight
                                    html_content = syntax_highlight(html_content)
                                    # write to file
                                    tmp_file.write(html_content)
                                    write_footer(tmp_file)
                                    post_file.close()
                        except Exception as error:
                            # print(traceback.format_exc())
                            pass
                # write page title
                dir_page.write(f"<h1>{dir_.title()}</h1>")
                if FLAG_DESC: dir_page.write(f"<p>{FLAG_DESC}</p>")
                # write posts index
                generate_post_index(dir_page, FLAG_SORT, FLAG_COL, posts_lst, posts_dict)
                # write footer
                write_footer(dir_page)

    # create html page for each md file in pages folder
    for root, dirs, files in os.walk(f"{SOURCE_PATH}/pages"):
        for file in files:
            FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
            if file.split(".")[1] == "md":
                file_name = file.split(".")[0]
                # create page
                with open(f"{DIST_PATH}/{file_name}.html", "w+") as tmp_file:
                    file = open(f"{root}/{file}", "r")
                    file_content = file.read()
                    file_content = file_content.split("\n")
                    # flags
                    if (file_content[0].startswith("-* ")):
                        FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = parse_flags(file_content[0])
                        # skip empty line following flags (if any)
                        if (len(file_content[1]) == 0):
                            file_content = file_content[2:]
                        else:
                            file_content = file_content[1:]
                    # find and use first line starting with # as title
                    title = PAGE_TITLE
                    for line in file_content:
                        if line.startswith("# "):
                            title = line.split("# ")[1]
                            # remove links in title
                            title = title.split("[")[0]
                            break
                    # join 
                    file_content = "\n".join(file_content)
                    # add updated time
                    if FLAG_TIME: file_content = re.sub(r"# (.*)", r"#\1" + f"\n*Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*", file_content, count=1)
                    # generate anchors and inject index
                    if FLAG_TOC: file_content = generate_and_inject_index(file_content)
                    # write header
                    write_header(tmp_file, title)
                    # replace -- with &mdash;
                    file_content = re.sub(r" -- (.*)", r" &mdash; \1", file_content)
                    # convert markdown to html
                    file_content = markdown.markdown(file_content, extensions=["fenced_code", "tables"])
                    # replace hr with border (for table of contents)
                    file_content = replace_hr_with_border(file_content, toc=True)
                    # generate checklist from list
                    file_content = generate_checklist_from_list(file_content)
                    # syntax highlight
                    file_content = syntax_highlight(file_content)
                    # write to file
                    tmp_file.write(file_content)
                    # list recent posts on index
                    if POSTS_ON_INDEX and file_name == "index":
                        tmp_file.write("<hr>")
                        generate_post_index(tmp_file, FLAG_SORT, FLAG_COL, GLOBAL_POSTS)
                    if FLAG_COL: tmp_file.write("</div>")
                    write_footer(tmp_file)
                    file.close()

if __name__ == "__main__":
    SOURCE_PATH = sys.path[0] + sys.argv[1] if len(sys.argv) > 1 else None
    if not SOURCE_PATH == None:
        DIST_PATH = sys.path[0] + DIST_PATH
        main_driver()
    else:
        print("SOURCE_PATH missing -> python md2mono.py /website")
