document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
  const mainNav = document.querySelector(".main-nav")

  if (mobileMenuToggle && mainNav) {
    mobileMenuToggle.addEventListener("click", function () {
      mainNav.classList.toggle("active")
      this.classList.toggle("active")
    })
  }

  // Category filter
  const categorySelect = document.getElementById("category")
  if (categorySelect) {
    categorySelect.addEventListener("change", function () {
      const url = new URL(window.location)
      url.searchParams.set("category", this.value)
      url.searchParams.delete("page")
      window.location = url
    })
  }

  // Sort filter
  const sortSelect = document.getElementById("sort")
  if (sortSelect) {
    sortSelect.addEventListener("change", function () {
      const url = new URL(window.location)
      url.searchParams.set("sort", this.value)
      url.searchParams.delete("page")
      window.location = url
    })
  }
})
