function change() {
    var modelCbs = document.querySelectorAll(".mycategories input[type='checkbox']");
    var filters = {
      models: getClassOfCheckedCheckboxes(modelCbs),
    };
  console.log(filters);
    filterResults(filters);
  }
  
  function getClassOfCheckedCheckboxes(checkboxes) {
    var classes = [];
  
    if (checkboxes && checkboxes.length > 0) {
      for (var i = 0; i < checkboxes.length; i++) {
        var cb = checkboxes[i];
  
        if (cb.checked) {
          classes.push(cb.getAttribute("rel"));
        }
      }
    }
  
    return classes;
  }
  
  function filterResults(filters) {
    var rElems = document.querySelectorAll("div .category");
    var hiddenElems = [];
  
    if (!rElems || rElems.length <= 0) {
      return;
    }
  
    for (var i = 0; i < rElems.length; i++) {
      var el = rElems[i];
        //console.log(el);
      if (filters.models.length > 0) {
        var isHidden = true;
  
        for (var j = 0; j < filters.models.length; j++) {
          var filter = filters.models[j];
  
          if (el.classList.contains(filter)) {
            isHidden = false;
            console.log("Shown");
            break;
          }
        }
  
        if (isHidden) {
          hiddenElems.push(el);
        }
        
      }
      
    }
    console.log(hiddenElems);

    for (var i = 0; i < rElems.length; i++) {
      rElems[i].style.display = "block";
    }
    if (hiddenElems.length <= 0) {
      return;
    }
  
    for (var i = 0; i < hiddenElems.length; i++) {
      hiddenElems[i].style.display = "none";
    }
  }