#!/usr/bin/env zsh

if [ -z "$TMUX" ]; then

  tmux attach -t main || tmux new -s main

fi

export LANG=en_US.UTF-8
export BREW=$(brew --prefix)
export EDITOR='nvim'
export ZSH_THEME="powerlevel9k/powerlevel9k"
export ZSH="$HOME/.oh-my-zsh"

source $ZSH/oh-my-zsh.sh
source "$HOME/.spaceshiprc"
source $(brew --prefix)"/opt/zsh-git-prompt/zshrc.sh"

fpath+=($BREW/share/zsh-completions $HOME/zsh-completions/src $BREW/share/zsh/site-functions $BREW/share/zsh/site-functions/ $fpath)

if type brew &>/dev/null; then
  FPATH=$BREW/share/zsh-completions:$FPATH
  autoload -Uz compinit
  compinit
fi

source $HOME/zsh-hist/zsh-hist.plugin.zsh
source $BREW/share/zsh-navigation-tools/zsh-navigation-tools.plugin.zsh
source $HOME/.zcolors
source $HOME/zcolors/zcolors.plugin.zsh
source $HOME/zsh-completions/zsh-completions.plugin.zsh
alias nmac="sudo ifconfig en0 ether $(openssl rand -hex 6 | sed 's%\(..\)%\1:%g; s%.$%%')"
fpath+=($BREW/share/zsh-completions $HOME/zsh-completions/src $BREW/share/zsh/site-functions $BREW/share/zsh/site-functions/ $fpath)

if type brew &>/dev/null; then
  FPATH=$BREW/share/zsh-completions:$FPATH
  autoload -Uz compinit
  compinit
fi

source $HOME/zsh-hist/zsh-hist.plugin.zsh
source $BREW/share/zsh-navigation-tools/zsh-navigation-tools.plugin.zsh
source $HOME/.zcolors
source $HOME/zcolors/zcolors.plugin.zsh
source $HOME/zsh-completions/zsh-completions.plugin.zsh

alias nmac="sudo ifconfig en0 ether $(openssl rand -hex 6 | sed 's%\(..\)%\1:%g; s%.$%%')"
alias gilf="git log --stat=76,78 --minimal --name-only --graph --pretty=format:'%Cred%h%Creset %C(yellow)%d%Creset %s %Cgreen(%cr)%Creset %C(bold blue)<%an>%Creset' --abbrev-commi"

function gig() {
  git log --stat=76,78 --minimal --name-only --graph --pretty=format:'%Cred%h%Creset %C(yellow)%d%Creset %s %Cgreen(%cr)%Creset %C(bold blue)<%an>%Creset' --abbrev-commi $* | less -R
}
# Checkout a local branch, or create it if it doesn't exist yet
function gcl() {
  git checkout -B $1 origin/$1
}

# Create a new tag
alias gtt="git tag --track"
# List tags
# Create a new tag
# Delete the specified tag

alias gilf="git log --stat=76,78 --minimal --name-only --graph --pretty=format:'%Cred%h%Creset %C(yellow)%d%Creset %s %Cgreen(%cr)%Creset %C(bold blue)<%an>%Creset' --abbrev-commit"
alias gaa="git add -A"
alias gau="git add -u"
alias gb="git branch"
alias gba="git branch -a"
alias gc="git checkout"
alias gcam="git commit -am"
alias gcmsg="git commit -m"
alias gd="git diff"
alias gdcw="git diff --cached --word-diff"
alias gdca="git diff --cached"
alias gds="git diff --staged"
alias gdsv="git diff --staged --verbose"
alias gdv="git diff --verbose"
alias gdw="git diff --word-diff"
alias gf="git fetch"
alias gg="git grep"
alias gm="git merge"
alias gma="git merge --abort"
alias gmm="git merge master"
alias gmt="git mergetool"
alias gmv="git mv"
alias gp="git pull"
alias gpf="git push --force-with-lease"
alias gpl="git pull"
alias gpr="git pull --rebase"
alias gps="git push"
alias gpsu="git push --set-upstream"
alias gpsf="git push --force-with-lease"
alias gpsff="git push --force"
alias grb="git rebase"
alias grbc="git rebase --continue"
alias grbi="git rebase --interactive"
alias grbo="git rebase --onto"
alias grh="git reset HEAD"
alias grhh="git reset HEAD --hard"
alias gri="git rebase --interactive"
alias grm="git rm"
alias grmc="git rm --cached"
alias grmv="git remote rename"
alias grr="git remote remove"
alias grs="git reset"
alias grset="git remote set-url"
alias grt="cd \$(git rev-parse --show-toplevel || echo .)"
alias gru="git reset --"
alias grup="git remote update"
alias grv="git remote -v"
alias gsb="git status -sb"
alias gsd="git svn dcommit"
alias gsh="git show"
alias gsi="git submodule init"
alias gsps="git show --pretty=short --show-signature"
alias gsr="git svn rebase"
alias gss="git status -s"
alias gst="git status"
alias gsta="git stash"
alias gstaa="git stash apply"
alias gstd="git stash drop"
alias gstl="git stash list"
alias gstp="git stash pop"
alias gsts="git stash show --text"
alias gsu="git submodule update"
alias gts="git tag -s"
alias gtv="git tag | sort -V"
alias gunignore="git update-index --no-assume-unchanged"
alias gunwip="git log -n 1 | grep -q -c '--wip--' && git reset HEAD~1"
alias gup="git pull --rebase"
alias gupv="git pull --rebase -v"
alias gwch="git whatchanged -p --abbrev-commit --pretty=medium"
alias gwip="git add -A; git ls-files --dez | xargs -0 git rm; git --no-verify --no-gpg-sign -m '--wip--'"

# gfind, locate aliases
alias gfind='git ls-files -z | xargs -0 grep -I'
alias gfindi='git ls-files -z | xargs -0 grep -i'
alias gfindc='git ls-files -z | xargs -0 grep -i -c'
alias gfindw='git ls-files -z | xargs -0 grep -i -w'
alias gfindwc='git ls-files -z | xargs -0 grep -i -wc'
alias glocate='git ls-files -z | xargs -0 grep -i -l'
alias glocatew='git ls-files -z | xargs -0 grep -i -w -l'

# coreutils aliases macos


function gig() {
  if [ $# -eq 0 ]; then
    echo "Usage: gig <technology> [technology] ..."
    return
  fi
  if [ "$1" = "-L" ]; then
    response=$(curl -L -s "https://www.gitignore.io/api/list")
    echo $response | tr "\\n" "," | tr "," "\n" | less
    return
  fi

  # curl -L -s "https://www.gitignore.io/api/$@"

  local url="https://www.gitignore.io/api/${technologies[0]}"
  for ((i = 1; i < ${#technologies[@]}; i++)); do
    url+=",${technologies[$i]}"
  done

  local response
  response=$(curl -L -s "$url")
  if [ $? -ne 0 ]; then
    echo "curl failed: $?"
    return
  fi

  local response_code
  response_code=$(echo "$response" | head -1)
  if [ "$response_code" != "200" ]; then
    echo "Unexpected response from curl: $response"
    return
  fi

  echo "$response"
}


alias ls="gls --all --group-directories-first --format long --sort=time  --time=ctime --color=tty --literal --time-style=locale -hFHLG"
alias vi=nvim
alias airport='/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
alias zshed="nvim $HOME/.zshrc"
alias twanz="cd /Users/twanz/Documents/Github/twanz"
alias projects="cd /Users/twanz/Documents"
alias sh=zsh
alias s=zsh
alias 1fz="gfind . -size 0"
alias 1fss="gfind . -type s -ls"
alias 1fs="gfind . -type s"
alias 1fll="gfind . -type l -ls"
alias 1fl="gfind . -type l"
alias 1ff="gfind . -type f"
alias 1fexe="gfind . -type f -perm +111"
alias 1fe="gfind . -empty"
alias 1fd="gfind . -type d"
alias 1f8="gfind . -size +1G"
alias 1f7="gfind . -size +100M"
alias 1f6="gfind . -size +10M"
alias 1f5="gfind . -size +1M"
alias 1f4="gfind . -size +100k"
alias 1f3="gfind . -size +10k"
alias 1f2="gfind . -size +1k"
alias 1f1="gfind . -size +0"
alias 1f="gfind . -type f -o -type d"
alias 1f-xdev="gfind . -type f -xdev"
alias 1f-xdev-="gfind . -type f !xdev"
alias 1f-xdev-="gfind . -type f ! -xdev"
alias 1f-writable="gfind . -type f -writable"
alias 1f-writable-="gfind . -type f ! -writable"
alias 1f-wholename="gfind . -type f -wholename"
alias 1f-wholename-="gfind . -type f ! -wholename"
alias 1f-user="gfind . -type f -user"
alias 1f-user-="gfind . -type f ! -user"
alias 1f-uid="gfind . -type f -uid"
alias 1f-uid-="gfind . -type f ! -uid"
alias 1f-true="gfind . -type f -true"
alias 1f-true-="gfind . -type f ! -true"
alias 1f-size="gfind . -type f -size"
alias 1f-size="gfind . -type f -size +1M"
alias 1f-size-="gfind . -type f ! -size"
alias 1f-size-="gfind . -type f -size -1M"
alias 1f-samefile="gfind . -type f -samefile"
alias 1f-samefile-="gfind . -type f ! -samefile"
alias 1f-regex="gfind . -type f -regex"
alias 1f-regex-="gfind . -type f ! -regex"
alias 1f-readable="gfind . -type f -readable"
alias 1f-readable-="gfind . -type f ! -readable"
alias 1f-prune="gfind . -type f -prune"
alias 1f-prune-="gfind . -type f ! -prune"
alias 1f-printf="gfind . -type f -printf"
alias 1f-printf-="gfind . -type f ! -printf"
alias 1f-printdir="gfind . -type f -printdir"
alias 1f-printdir-="gfind . -type f ! -printdir"
alias 1f-print0="gfind . -type f -print0"
alias 1f-print0-="gfind . -type f ! -print0"
alias 1f-print="gfind . -type f -print"
alias 1f-print-="gfind . -type f ! -print"
alias 1f-perm="gfind . -type f -perm"
alias 1f-perm-="gfind . -type f ! -perm"
alias 1f-path="gfind . -type f -path"
alias 1f-path-="gfind . -type f ! -path"
alias 1f-okdir="gfind . -type f -okdir"
alias 1f-okdir-="gfind . -type f ! -okdir"
alias 1f-ok="gfind . -type f -ok"
alias 1f-ok-="gfind . -type f ! -ok"
alias 1f-newer="gfind . -type f -newer"
alias 1f-newer-="gfind . -type f ! -newer"
alias 1f-name="gfind . -type f -name"
alias 1f-name-="gfind . -type f ! -name"
alias 1f-mtime="gfind . -type f -mtime"
alias 1f-mtime="gfind . -type f -mtime +90"
alias 1f-mtime-="gfind . -type f ! -mtime"
alias 1f-mtime-="gfind . -type f -mtime -90"
alias 1f-mount="gfind . -type f -mount"
alias 1f-mount-="gfind . -type f ! -mount"
alias 1f-mmin="gfind . -type f -mmin"
alias 1f-mmin-="gfind . -type f ! -mmin"
alias 1f-mindepth="gfind . -type f -mindepth"
alias 1f-mindepth-="gfind . -type f ! -mindepth"
alias 1f-maxdepth="gfind . -type f -maxdepth"
alias 1f-maxdepth-="gfind . -type f ! -maxdepth"
alias 1f-ls="gfind . -type f -ls"
alias 1f-ls-="gfind . -type f ! -ls"
alias 1f-links="gfind . -type f -links"
alias 1f-links-="gfind . -type f ! -links"
alias 1f-iregex="gfind . -type f -iregex"
alias 1f-iregex-="gfind . -type f ! -iregex"
alias 1f-ipath="gfind . -type f -ipath"
alias 1f-ipath-="gfind . -type f ! -ipath"
alias 1f-inum="gfind . -type f -inum"
alias 1f-inum-="gfind . -type f ! -inum"
alias 1f-iname="gfind . -type f -iname"
alias 1f-iname-="gfind . -type f ! -iname"
alias 1f-group="gfind . -type f -group"
alias 1f-group-="gfind . -type f ! -group"
alias 1f-gid="gfind . -type f -gid"
alias 1f-gid-="gfind . -type f ! -gid"
alias 1f-fprintf="gfind . -type f -fprintf"
alias 1f-fprintf-="gfind . -type f ! -fprintf"
alias 1f-fprint0="gfind . -type f -fprint0"
alias 1f-fprint0-="gfind . -type f ! -fprint0"
alias 1f-fprint="gfind . -type f -fprint"
alias 1f-fprint-="gfind . -type f ! -fprint"
alias 1f-follow="gfind . -type f -follow"
alias 1f-follow="g . -type f -follow"
alias 1f-follow-="gfind . -type f ! -follow"
alias 1f-fls="gfind . -type f -fls"
alias 1f-fls-="gfind . -type f ! -fls"
alias 1f-false="gfind . -type f -false"
alias 1f-false-="gfind . -type f ! -false"
alias 1f-executable="gfind . -type f -executable"
alias 1f-executable-="gfind . -type f ! -executable"
alias 1f-execdir="gfind . -type f -execdir"
alias 1f-execdir-="gfind . -type f ! -execdir"
alias 1f-exec="gfind . -type f -exec"
alias 1f-exec-="gfind . -type f ! -exec"
alias 1f-exe="gfind . -type f ! -perm +111"
alias 1f-empty="gfind . -type f -empty"
alias 1f-empty-="gfind . -type f ! -empty"
alias 1f-depth="gfind . -type f -depth"
alias 1f-depth-="gfind . -type f ! -depth"
alias 1f-delete="gfind . -type f -delete"
alias 1f-delete-="gfind . -type f ! -delete"
alias 1f-ctime="gfind . -type f -ctime"
alias 1f-ctime="gfind . -type f -ctime +90"
alias 1f-ctime-="gfind . -type f ! -ctime"
alias 1f-ctime-="gfind . -type f -ctime -90"
alias 1f-cnewer="gfind . -type f -cnewer"
alias 1f-cnewer-="gfind . -type f ! -cnewer"
alias 1f-cmin="gfind . -type f -cmin"
alias 1f-cmin-="gfind . -type f ! -cmin"
alias 1f-atime="gfind . -type f -atime"
alias 1f-atime="gfind . -type f -atime +90"
alias 1f-atime-="gfind . -type f ! -atime"
alias 1f-atime-="gfind . -type f -atime -90"
alias 1f-anewer="gfind . -type f -anewer"
alias 1f-anewer-="gfind . -type f ! -anewer"
alias 1f-amin="gfind . -type f -amin"
alias 1f-amin-="gfind . -type f ! -amin"
# find aliases


alias nmac="sudo ifconfig en0 ether $(openssl rand -hex 6 | sed 's%\(..\)%\1:%g; s%.$%%')"
alias ls="gls --all --group-directories-first --format long --sort=time  --time=ctime --color=tty --literal --time-style=locale -hFHLG"
alias vi=nvim
alias airport='/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
alias zshed="nvim $HOME/.zshrc"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

autoload -U add-zsh-hook
load-nvmrc() {
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$(nvm version)" ]; then
      nvm use
    fi
  elif [ -n "$(PWD=$OLDPWD nvm_find_nvmrc)" ] && [ "$(nvm version)" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc

bindkey '^[[1;4C' forward-word
bindkey '^[[1;4D' backward-word
WORDCHARS='~!@#$%^&*()_+|-=`{}[]:";<>?,./'
MOTION_WORDCHARS='~!@#$%^&*()_+|-=`{}[]:";<>?,./'

zstyle 'completion:*' menu select=2
zstyle ':completion:*' verbose yes
zstyle ':completion:*' verbose true
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' use-cache on
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' select-prompt '%SScrolling active: current selection at %p%s'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' max-errors numeric
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' list-prompt '%SAt %p: Hit TAB for more, or the character to insert%s'
zstyle ':completion:*' list-prompt '%S%M matches%s'
zstyle ':completion:*' list-prompt
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' group-order groups=- all-files files-without-match files-with-matches
zstyle ':completion:*' group-name ''
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' completer _expand _complete _ignored _match _approximate
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' cache-path $ZSH/cache/$HOST
zstyle ':completion:*:warnings' format '%BSorry, no matches for: %d%b'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'
zstyle ':completion:*:descriptions' format '%B%d%b'
zstyle ':completion:*:default' list-prompt '%S%M matches%s'
zstyle ':completion:*:corrections' format '%B%d (errors: %e)%b'
zstyle ':completion:*:*:kill:*' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'
zstyle ':completion:*:*:*:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'
zstyle ':completion:*:*:*:*:processes' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'
zstyle ':completion:*:*:*:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'

STARSHIPINIT=$(/usr/local/bin/starship init zsh --print-full-init)
eval "$(starship init zsh)"

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

__conda_setup="$('/usr/local/Caskroom/miniconda/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/local/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
        . "/usr/local/Caskroom/miniconda/base/etc/profile.d/conda.sh"
    else
        export PATH="/usr/local/Caskroom/miniconda/base/bin:$PATH"
    fi
fi
unset __conda_setup

if [ -f '/Users/twanz/Library/Application Support/cloud-code/installer/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/twanz/Library/Application Support/cloud-code/installer/google-cloud-sdk/path.zsh.inc'; fi


if [ -f '/Users/twanz/Library/Application Support/cloud-code/installer/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/twanz/Library/Application Support/cloud-code/installer/google-cloud-sdk/completion.zsh.inc'; fi



# source /Users/twanz/spaceship-prompt/spaceship.zsh
export PATH=/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH
