document.addEventListener("DOMContentLoaded", () => {
  // الحصول على زر تبديل الوضع
  const themeToggle = document.getElementById("theme-toggle")
  const sunIcon = document.getElementById("sun-icon")
  const moonIcon = document.getElementById("moon-icon")

  // التحقق من وجود تفضيل محفوظ
  const savedTheme = localStorage.getItem("theme")

  // التحقق من تفضيل النظام
  const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)")

  // تعيين الوضع الافتراضي بناءً على التفضيل المحفوظ أو تفضيل النظام
  if (savedTheme) {
    document.documentElement.setAttribute("data-theme", savedTheme)
    updateIcons(savedTheme)
  } else if (prefersDarkScheme.matches) {
    document.documentElement.setAttribute("data-theme", "dark")
    updateIcons("dark")
  }

  // تحديث الأيقونات بناءً على الوضع الحالي
  function updateIcons(theme) {
    if (theme === "dark") {
      moonIcon.style.display = "none"
      sunIcon.style.display = "block"
    } else {
      moonIcon.style.display = "block"
      sunIcon.style.display = "none"
    }
  }

  // إضافة مستمع حدث لزر تبديل الوضع
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      // الحصول على الوضع الحالي
      const currentTheme = document.documentElement.getAttribute("data-theme") || "light"

      // تبديل الوضع
      const newTheme = currentTheme === "light" ? "dark" : "light"

      // تحديث السمة وحفظ التفضيل
      document.documentElement.setAttribute("data-theme", newTheme)
      localStorage.setItem("theme", newTheme)

      // تحديث الأيقونات
      updateIcons(newTheme)
    })
  }

  // الاستماع لتغييرات في تفضيل النظام
  prefersDarkScheme.addEventListener("change", (e) => {
    // إذا لم يكن هناك تفضيل محفوظ، اتبع تفضيل النظام
    if (!localStorage.getItem("theme")) {
      const newTheme = e.matches ? "dark" : "light"
      document.documentElement.setAttribute("data-theme", newTheme)
      updateIcons(newTheme)
    }
  })
})
