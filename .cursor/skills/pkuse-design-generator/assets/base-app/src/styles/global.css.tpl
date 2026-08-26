[data-pkuse-app="__APP_NAME__"] {
  min-height: 100%;
  font-family: var(--__APP_PREFIX__-font-family);
}

[data-pkuse-app="__APP_NAME__"] .pkuse-shell {
  min-height: 100vh;
}

[data-pkuse-app="__APP_NAME__"] .pkuse-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: var(--__APP_PREFIX__-padding-lg);
}

[data-pkuse-app="__APP_NAME__"] .pkuse-brand,
[data-pkuse-app="__APP_NAME__"] .pkuse-user,
[data-pkuse-app="__APP_NAME__"] .pkuse-header a {
  color: var(--__APP_PREFIX__-color-text-light-solid);
}

[data-pkuse-app="__APP_NAME__"] .pkuse-content {
  padding: var(--__APP_PREFIX__-padding-lg);
}

[data-pkuse-app="__APP_NAME__"] :focus-visible {
  outline: var(--__APP_PREFIX__-line-width-focus) solid
    var(--__APP_PREFIX__-color-primary-border);
  outline-offset: var(--__APP_PREFIX__-control-outline-width);
}
