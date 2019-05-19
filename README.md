# MDiocre

A very simple static website generator tool powered by Python and Pandoc. Powered by Markdown (will expand to other markup later). Currently not tag-aware. Minimal setup. Image support limited to jpg/jpeg, png, gif.

## Requirements
* Python 3 (+pypandoc, colorama)
* Pandoc

## What sets it apart from other tools?

It's terrible and it doesn't have a profitable and pragmatic usecase in mind, but it works okay. For my needs, anyway. It's alright for simple blogs with no tagging and very simple static websites.

## MDiocre terminology

* **Modules** - Essentially subfolders of your website for various types of content. Such as blogs, pages, plans or anything else.
* **Website Configuration** - Sitewide settings. You can set (global!) variable names here, such as your site name. You can also set the source folder, build folder, and a folder for templates.
* **Application Configuration** - The settings used within the MDiocre console application. Sets the website configuration to use, whether or not to have detailed output, whether or not to include raw HTML files, etc.

## How do I make a site with this?

1. After cloning/downloading this repo (extracting it to a folder called `MDiocre`), create a work folder adjacent to that folder. Let's call it `work` for now.
2. Copy the default `mdiocre.ini` to that folder.
3. Create a folder called `site`.
4. In that folder, create a file called `site.ini` with the following contents:
```
[config]
modules         = root, pages
use-templates   = main
source-folder   = site/_src
build-folder    = site/built
template-folder = site/_templates

[vars]
site-name       = My Homepage
```
5. Then make two more folders in the same location with the names `_src` and `_templates`.
6. Make a file called `main.html` inside `_templates` with these contents:
```
<html>
<head>Welcome to <!--var:site-name-->!</head>
<body><!--var:content--></body>
</html>
```
7. Make a file called `index.md` inside of `_src` and write anything on it.
8. Inside `_src`, create a folder named `pages` and make a file in it called `index.template` that contains the following:
```
<!--var:content-->
```
9. In that same folder, write a bunch of different text files - but it must have the `.md` extension!
10. Go back 2 levels to your `work` folder. Assuming Python is present in your PATH (environment variable), create a new text document containing:
```
python3 ../MDiocre/mdiocre_console.py -C mdiocre.ini build
```
Save it inside the folder as a .bat if you're on Windows, or as a .sh if you're on Mac, Linux, or other Unix-like systems. Double click or execute it.

11. Check the `site/built` folder.

## What the hell did I just do?

1. You were extracting the repository containing MDiocre.
2. You have set the application configuration. You can now change it at will.
3. The `site` folder happened to be the folder that was set in the application configuration.
4. You have set the site configuration. Change this to suit your website. FYI: The `root` module is simply the root folder of your website, in this case, the build directory.
5. Creating the folders defined in the site configuration, except for `built`, as that will be created automatically when you build the site.
6. Creating the template. This is a standard HTML document. You can set and get variables here in the form of HTML comments. See section **Variables** for more info. The `content` variable simply contains the contents of your page, so do not set this variable manually!
7. Creating the home page. As a standard, a website's homepage is simply called `index.html`. So, to generate that file, we need to make a `index.md`.
8. You have created an index template for the `pages` module. Unlike the template you made in step 6, this is a *Markdown* formatted template. This will be what the module's `index.html` be based on. The `content` variable will include a simple listing of the pages. The purpose of this template is that so you can add descriptions, additional styles, etc.
9. You have written a bunch of random articles. If the module it resides in are indexed, it will show up on the index page. In it, if you have set the `title` variable on a page, then the page will be listed with whatever `title` is, and not the filename of the page.

   If you have set the `date` as well, it will display the date on it. I recommend you use the [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, especially for a blog. Such a format will ensure that the index will sort by date correctly. (Yes, it is unfortunately not smart enough to recognize different date formats yet!)
10. Building the website.
11. Enjoying your built website.

## Precautions

* mdiocre.ini
  
  You just need to specify a path to the config and logfile. Make sure any subfolders exist beforehand!
  
* site.ini
  
  Paths to subfolders are **RELATIVE** to the directory on which `mdiocre_console.py` is run on.

* Code blocks where it happens to match MDiocre commands will **NOT** be spared. Known bug.

* Your page's contents will be in the `content` variable, so **DO NOT** set this manually!


## Variables

MDiocre allows setting variables for the site. Keep in mind that these are **global** at the moment, meaning that any variable you set will be visible throughout the whole website. These variables are parsed according to the order that MDiocre builds the pages in (sorted), so be careful.

**Setting a variable to a string**
```
<!--hello="test message"-->
```
Simply sets `hello` to `test message`.


**Setting a variable to another variable**
```
<!--hello=lemons-->
```
If `lemons` is `1` then `hello` will also be `1`. Otherwise, `hello` will contain the string `lemons`.

**Concatenating two or more variables**
```
<!--lemons=hello, hello-->
```
If `hello` contains `abc` then `lemons` will contain `abcabc`. However, if you also include a space string in between, like this...
```
<!--lemons=hello," ",hello-->
```
`lemons` will contain `abc abc`!