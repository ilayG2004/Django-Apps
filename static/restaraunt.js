function show_extra() {
  const sandwich = document.getElementById("sandwichCheckbox");
  const pickles = document.getElementById("pickleOptions");

  if (sandwich.checked) {
    pickles.style.display = "block";
  } else {
    pickles.style.display = "none";
  }
}