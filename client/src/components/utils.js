export function isElementInViewport(el) {
  var rect = el.getBoundingClientRect()

  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  )
}

export function scrollIntoView(el, offsetY = 0) {
  if (isElementInViewport(el)) return

  const { bottom } = el.getBoundingClientRect()
  const newScrollPos =
    window.scrollY +
    bottom -
    (window.innerHeight || document.documentElement.clientHeight) +
    offsetY
  scrollTo(0, newScrollPos)
}

export function pluralize(count, word, pluralWord) {
  return `${count} ${count === 1 ? word : pluralWord}`
}
