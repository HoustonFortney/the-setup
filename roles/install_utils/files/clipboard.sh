# Command line clipboard utilities
yank() {
  if [[ -t 0 ]]; then
    # Input is not a pipe, copy from specified file
    cat "$@" | xclip -selection clipboard
  else
    # Input is from a pipe, copy the piped content and pass it through
    tee >(xclip -selection clipboard)
  fi
}
yank-wd() {
  # Copy the current working directory
  pwd | yank
}
yank-cmd() {
  # Copy the last command
  fc -ln -1 | sed 's/^[[:space:]]*//' | yank
}
put() {
  # Paste from clipboard
  xclip -selection clipboard -o
}
alias ywd='yank-wd'
alias ycmd='yank-cmd'
