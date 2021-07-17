def delete_navi_bar(driver):
    """Delete navigation of page for capturing clear image.
    """
    js_string = """
    function f() {
   var x = document.getElementsByClassName("manga-bottom-navi");
        for(var i = x.length - 1; i >= 0; i--) {
        x[i].parentNode.removeChild(x[i]);
        }
    }

    f();
    """
    driver.execute_script(js_string)

def delete_thumbnail_list(driver):
    """Delete thumbnail list of page.
    Thumbnail list includes many img elements.
    Som, 
    """
    js_string = """
    function f() {
   var x = document.getElementsByClassName("list-container");
        for(var i = x.length - 1; i >= 0; i--) {
        x[i].parentNode.removeChild(x[i]);
        }
    }

    f();
    """
    driver.execute_script(js_string)