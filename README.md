![acid.nvim](https://raw.githubusercontent.com/clojure-vim/acid.nvim/master/acidnvim.png)

Asynchronous Clojure Interactive Development

## What is it for?

Acid.nvim is a plugin for clojure development on neovim.
It was initially designed within [iron.nvim](http://github.com/clojure-vim/iron.nvim), but evolved to be a proper clojure plugin for neovim.

## Design and Structure

It is built fundamentally on neovims async capabilities and rely deeply on clojures
[refactor-nrepl](https://github.com/clojure-emacs/refactor-nrepl) and
[nrepl-python-client](https://github.com/cemerick/nrepl-python-client).

## Installing

First, install the python dependencies:

```bash
pip3 install --user neovim
```

Update your `~/.lein/profiles.clj` adding the following lines:
```clj
[refactor-nrepl "2.3.0-SNAPSHOT"]
[cider/cider-nrepl "0.14.0"]
```

Then, add and install acid:

```vim
Plug 'clojure-vim/acid.nvim', { 'do': ':UpdateRemotePlugins' }
```

Acid is a remote plugin. This means it communicates with neovim using the rpc interface.

## Running

Acid has some commands for interacting with the nrepl.

Currently, there is no documentation for those commands, but a few are worth
mentioning here:

* `<leader>N` Creates a new file
* `K` Shows documentation for the symbol below cursor
* `car` Requires current file
* `caR` Requires dependency line below cursor (i.e. `[clojure.string :as str]`)
* `gu` Shows usage of symbol below cursor
* `gd` Goes to definition of symbol below cursor
* `cp<motion>` Sends the block to nrepl for evaluation
* `cpp` Shorthand mapping for evaluating the whole block below cursor (up until the outermost)

All those are defined as Commands as well:

* `AcidNewFile <ns.file>` Creates a new file under supplied ns.name.
* `AcidNewFilePrompt` Prompts for the full filename for creation.
* `AcidLoadAll` Loads all project namespaces into the nrepl for easier navigation.
* `AcidRequire [<require> [<options>]]` Requires a namespace.
  * If no parameters supplied, loads current ns.
  * Arguments supplied can be the same as a require vector, taking options:
    * `AcidRequire clojure.string :as str`
    * `AcidRequire clojure.string :refer [join]`
* `AcidDoc <ns/symbol>` Shows the documentation of the supplied symbol.

There are a few more which are unstable and/or incomplete.

## Cool, I want more


Take a look at the [design](https://github.com/clojure-vim/acid.nvim/blob/master/DESIGN.md) page
for a better understanding on how acid works.

Acid is growing up in both complexity and features and there is still a lot of work to be done.
Please take a look at the [TODO](https://github.com/clojure-vim/acid.nvim/blob/master/TODO.md) for the roadmap.
