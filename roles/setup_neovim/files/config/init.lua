vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

vim.g.have_nerd_font = true

-- =========================
-- Options
-- =========================
local opt = vim.opt

opt.relativenumber = true
opt.smartindent = true
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true
opt.showmatch = true
opt.clipboard = "unnamedplus"
opt.scrolloff = 10
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.termguicolors = true
opt.signcolumn = "yes"
opt.list = true
opt.foldmethod = "expr"
opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
opt.foldlevel = 99
opt.fillchars:append({ eob = " " })
opt.winborder = "rounded"
opt.updatetime = 250
opt.autoread = true

-- =========================
-- Filetypes
-- =========================

vim.filetype.add({
    pattern = {
        [".*/templates/.*%.ya?ml"] = "helm",
    },
})

-- =========================
-- Autocommands
-- =========================

vim.api.nvim_create_autocmd("BufReadPost", {
    desc = "Restore cursor position when reopening files",
    callback = function()
        local row, col = unpack(vim.api.nvim_buf_get_mark(0, '"'))
        if row > 0 and row <= vim.api.nvim_buf_line_count(0) then
            pcall(vim.api.nvim_win_set_cursor, 0, { row, col })
        end
    end,
})

vim.api.nvim_create_autocmd("BufWritePre", {
    desc = "Create parent directories on save",
    callback = function(args)
        local dir = vim.fn.fnamemodify(args.file, ":p:h")
        if dir ~= "" then
            vim.fn.mkdir(dir, "p")
        end
    end,
})

vim.api.nvim_create_autocmd("FileType", {
    desc = "Close NvimTree and Undotree with Escape",
    pattern = { "NvimTree", "undotree" },
    callback = function(event)
        vim.keymap.set("n", "<Esc>", "<cmd>close<CR>", { buffer = event.buf, silent = true })
    end,
})

vim.api.nvim_create_autocmd("TextYankPost", {
    desc = "Highlight yanked text",
    callback = function()
        vim.highlight.on_yank({ higroup = "Visual", timeout = 200 })
    end,
})

vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter", "CursorHold", "CursorHoldI" }, {
    desc = "Check for external file changes",
    callback = function()
        if vim.fn.mode() ~= "c" and vim.fn.getcmdwintype() == "" then
            vim.cmd("checktime")
        end
    end,
})

vim.api.nvim_create_autocmd("FileChangedShell", {
    desc = "Force-reload externally changed files; local edits recoverable via undo (u)",
    callback = function()
        vim.v.fcs_choice = "reload"
    end,
})

vim.api.nvim_create_autocmd("FileChangedShellPost", {
    desc = "Notify after an externally-changed file is reloaded",
    callback = function()
        vim.notify("Buffer reloaded from disk (u to recover local edits)", vim.log.levels.WARN)
    end,
})

vim.api.nvim_create_autocmd("CursorHold", {
    desc = "Show diagnostics in a floating window on hover",
    callback = function()
        local opts = {
            focusable = false,
            close_events = { "BufLeave", "CursorMoved", "InsertEnter", "FocusLost" },
        }
        if #vim.diagnostic.get(0) > 0 then
            vim.diagnostic.open_float(nil, opts)
        end
    end,
})

-- =========================
-- Key mappings
-- =========================
vim.g.mapleader = " "
local map = vim.keymap.set

map("v", "J", ":m '>+1<CR>gv=gv", { desc = "Move selection down" })
map("v", "K", ":m '<-2<CR>gv=gv", { desc = "Move selection up" })

map("n", "<C-d>", "<C-d>zz", { desc = "Scroll down and center" })
map("n", "<C-u>", "<C-u>zz", { desc = "Scroll up and center" })
map("n", "n", "nzzzv", { desc = "Next search result and center" })
map("n", "N", "Nzzzv", { desc = "Previous search result and center" })

map("n", "<leader>r", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]], { desc = "Substitute word under cursor" })

map("x", "<leader>p", [["_dP]], { desc = "Paste without overwriting clipboard" })
map({ "n", "v" }, "<leader>d", [["_d]], { desc = "Delete without overwriting clipboard" })

map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear search highlighting" })

map("n", "<leader>qq", ":bufdo bwipeout<CR>", { desc = "Close all buffers" })

-- Quick run
local pedal_key = "<F2>"
map("n", pedal_key, function()
    vim.cmd("wa")
    vim.fn.jobstart("quick-run-go")
end, { silent = true })
map("i", pedal_key, function()
    vim.cmd("stopinsert")
    vim.cmd("wa")
    vim.fn.jobstart("quick-run-go")
end, { silent = true })

-- =========================
-- Bootstrap lazy.nvim
-- =========================
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable",
        lazypath,
    })
end

vim.opt.rtp:prepend(lazypath)

-- =========================
-- Plugins
-- =========================
require("lazy").setup({
    {
        "tpope/vim-surround",
        event = "VeryLazy",
    },
    {
        "nvim-treesitter/nvim-treesitter",
        build = ":TSUpdate",
        opts = {
            auto_install = true,
            highlight = {
                enable = true,
            },
            indent = {
                enable = true,
            },
        },
    },
    {
        "nvim-telescope/telescope.nvim",
        lazy = false, -- Required for compatibility with alpha-nvim
        keys = {
            { "<leader>sf", "<cmd>Telescope find_files<cr>", desc = "Search files" },
            { "<leader>sg", "<cmd>Telescope live_grep<cr>",  desc = "Search with grep" },
            { "<leader>sb", "<cmd>Telescope buffers<cr>",    desc = "Search in buffers" },
            { "<leader>sh", "<cmd>Telescope help_tags<cr>",  desc = "Search help tags" },
        },
        dependencies = {
            "nvim-lua/plenary.nvim",
            { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
            "nvim-telescope/telescope-ui-select.nvim",
        },
        config = function()
            local telescope = require("telescope")
            telescope.load_extension("fzf")
            telescope.load_extension("ui-select")
            telescope.setup({
                defaults = {
                    file_ignore_patterns = { "%.git/" },
                },
                pickers = {
                    find_files = {
                        hidden = true,
                    },
                },
                extensions = {
                    ["ui-select"] = {
                        require("telescope.themes").get_dropdown({
                            previewer = false,
                        }),
                    },
                },
            })
        end,
    },
    {
        "nvim-tree/nvim-tree.lua",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        keys = {
            { "<leader>e", "<cmd>NvimTreeToggle<CR>", desc = "Toggle file tree" },
        },
        config = function()
            require("nvim-tree").setup({
                view = {
                    float = {
                        enable = true,
                        open_win_config = function()
                            local screen_w = vim.opt.columns:get()
                            local screen_h = vim.opt.lines:get() - vim.opt.cmdheight:get()
                            local window_w = math.floor(screen_w * 0.8)
                            local window_h = math.floor(screen_h * 0.8)
                            local center_x = (screen_w - window_w) / 2
                            local center_y = ((vim.opt.lines:get() - window_h) / 2) - vim.opt.cmdheight:get()
                            return {
                                border = "rounded",
                                relative = "editor",
                                row = center_y,
                                col = center_x,
                                title = " Tree ",
                                title_pos = "center",
                                width = window_w,
                                height = window_h,
                            }
                        end,
                    },
                },
                actions = {
                    open_file = {
                        quit_on_open = true,
                    },
                },
            })
        end,
    },
    {
        "mbbill/undotree",
        keys = {
            { "<leader>u", "<cmd>UndotreeToggle<cr>", desc = "Toggle Undotree" },
        },
        init = function()
            vim.opt.undofile = true
            local undodir = vim.fn.stdpath("data") .. "/undo"
            if vim.fn.isdirectory(undodir) == 0 then
                vim.fn.mkdir(undodir, "p")
            end
            vim.opt.undodir = undodir
            vim.g.undotree_SetFocusWhenToggle = 1
        end,
    },
    {
        "tpope/vim-fugitive",
        cmd = { "Git", "G" },
    },
    {
        "lewis6991/gitsigns.nvim",
        event = { "BufReadPost", "BufNewFile" },
    },
    {
        "shortcuts/no-neck-pain.nvim",
        opts = {
            width = 120,
            autocmds = {
                enableOnVimEnter = true,
            },
        },
    },
    {
        "christoomey/vim-tmux-navigator",
        keys = {
            { "<C-h>", "<cmd>TmuxNavigateLeft<cr>",  desc = "Navigate to left tmux pane" },
            { "<C-j>", "<cmd>TmuxNavigateDown<cr>",  desc = "Navigate to down tmux pane" },
            { "<C-k>", "<cmd>TmuxNavigateUp<cr>",    desc = "Navigate to up tmux pane" },
            { "<C-l>", "<cmd>TmuxNavigateRight<cr>", desc = "Navigate to right tmux pane" },
        },
    },
    {
        "dracula/vim",
        name = "dracula",
        config = function()
            vim.cmd("colorscheme dracula")
            local dracula_foreground = "#f8f8f2"
            local dracula_background = "#21222c"
            local dracula_current_line = "#44475a" -- TODO: Highlight selected buffer
            local dracula_purple = "#bd93f9"
            -- Transparent background to reveal dark terminal background
            vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
            vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
            vim.api.nvim_set_hl(0, "WinSeparator", { bg = "none" })
            vim.api.nvim_set_hl(0, "Title", { fg = dracula_foreground })
            -- Customize the dracula theme for bufferline
            vim.api.nvim_set_hl(0, "BufferLineFill", { bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineBackground", { bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineCloseButton", { bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineCloseButtonSelected", { bg = dracula_background })
            vim.api.nvim_set_hl(
                0,
                "BufferLineBufferSelected",
                { fg = dracula_foreground, bg = dracula_background, bold = true }
            )
            vim.api.nvim_set_hl(0, "BufferLineSeparator", { bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineSeparatorSelected", { bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineIndicatorSelected", { fg = dracula_purple, bg = dracula_background })
            vim.api.nvim_set_hl(0, "BufferLineIconDefault", { fg = dracula_foreground, bg = dracula_background })
        end,
    },
    {
        "christopher-francisco/tmux-status.nvim",
        opts = {
            manage_tmux_status = false,
        },
    },
    {
        "nvim-lualine/lualine.nvim",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        config = function()
            -- Customize dracula theme for lualine
            local dracula = require("lualine.themes.dracula")
            local dracula_background = "#21222c"
            local dracula_current_line = "#44475a"
            local modes = { "normal", "insert", "visual", "replace", "command", "inactive" }
            for _, mode in ipairs(modes) do
                dracula[mode].b.bg = dracula_current_line
                dracula[mode].c.bg = dracula_background
            end
            require("lualine").setup({
                options = {
                    theme = dracula,
                    globalstatus = true,
                    section_separators = "",
                    component_separators = "",
                },
                sections = {
                    lualine_b = { "branch" },
                    lualine_c = { { "filename", file_status = true, path = 1 } },
                    lualine_x = { { require("tmux-status").tmux_session, cond = require("tmux-status").show } },
                    lualine_y = { "filetype" },
                },
            })
        end,
    },
    {
        "akinsho/bufferline.nvim",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        config = function()
            require("bufferline").setup({
                options = {
                    always_show_bufferline = false,
                    show_buffer_close_icons = false,
                },
            })
            map("n", "<A-h>", "<cmd>BufferLineCyclePrev<cr>", { desc = "Previous buffer" })
            map("n", "<A-l>", "<cmd>BufferLineCycleNext<cr>", { desc = "Next buffer" })
            map("n", "<A-S-h>", "<cmd>BufferLineMovePrev<cr>", { desc = "Move buffer left" })
            map("n", "<A-S-l>", "<cmd>BufferLineMoveNext<cr>", { desc = "Move buffer right" })
            map("n", "<A-q>", "<cmd>bdelete<cr>", { desc = "Close buffer" })
            map("n", "<A-p>", "<cmd>BufferLinePick<cr>", { desc = "Pick buffer" })
        end,
    },
    {
        "goolord/alpha-nvim",
        config = function()
            local dashboard = require("alpha.themes.dashboard")
            local header_art = {
                "███    ██ ███████  ██████  ██    ██ ██ ███    ███",
                "████   ██ ██      ██    ██ ██    ██ ██ ████  ████",
                "██ ██  ██ █████   ██    ██ ██    ██ ██ ██ ████ ██",
                "██  ██ ██ ██      ██    ██  ██  ██  ██ ██  ██  ██",
                "██   ████ ███████  ██████    ████   ██ ██      ██",
            }
            dashboard.section.header.val = header_art
            dashboard.section.header.opts = {
                position = "center",
            }
            dashboard.section.buttons.val = {
                dashboard.button("<leader>sf", "  Search for File", "<cmd>Telescope find_files<cr>"),
                dashboard.button("<leader>sg", "  Search with Grep", "<cmd>Telescope live_grep<cr>"),
            }
            local window_height = vim.api.nvim_win_get_height(0)
            local padding_height = math.max(0, math.floor((window_height - #header_art) / 2))
            local opts = {
                layout = {
                    { type = "padding", val = padding_height },
                    dashboard.section.header,
                    { type = "padding", val = 2 },
                    dashboard.section.buttons,
                    { type = "padding", val = window_height },
                },
                opts = { noautocmd = true },
            }
            require("alpha").setup(opts)
        end,
    },
    {
        "zbirenbaum/copilot.lua",
        lazy = false,
        opts = {
            suggestion = {
                auto_trigger = true,
                debounce = 50,
                keymap = {
                    accept = false,
                },
            },
            filetypes = {
                yaml = true,
                markdown = true,
                ["."] = true,
            },
        },
        config = function(_, opts)
            require("copilot").setup(opts)
            local suggestion = require("copilot.suggestion")
            map("i", "<Tab>", function()
                if suggestion.is_visible() then
                    return suggestion.accept()
                else
                    return "<Tab>"
                end
            end, { expr = true, silent = true, desc = "Accept Copilot suggestion" })
        end,
    },
    {
        "MeanderingProgrammer/render-markdown.nvim",
        dependencies = { "nvim-treesitter/nvim-treesitter", "nvim-tree/nvim-web-devicons" },
        opts = {},
    },
    {
        "williamboman/mason-lspconfig.nvim",
        dependencies = {
            "neovim/nvim-lspconfig",
            { "williamboman/mason.nvim", opts = {} },
        },
        opts = {
            ensure_installed = {
                -- Python
                "basedpyright",
                "ruff",
                -- C/C++
                "clangd",
                -- JavaScript/TypeScript
                "ts_ls",
                "eslint",
                -- Infrastructure
                "terraformls",
                "helm_ls",
                "dockerls",
                -- Verilog
                "verible",
                -- Protocols
                "buf_ls",
                -- Bash
                "bashls",
                -- Lua
                "lua_ls",
                -- General
                "jsonls",
                "yamlls",
                "marksman",
            },
        },
    },
    {
        "neovim/nvim-lspconfig",
        config = function()
            local on_attach = function(client, bufnr)
                local bufmap = function(mode, lhs, rhs, desc)
                    vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc })
                end

                local telescope_builtin = require("telescope.builtin")
                bufmap("n", "gd", telescope_builtin.lsp_definitions, "Go to definition")
                bufmap("n", "gi", telescope_builtin.lsp_implementations, "Go to implementation")
                bufmap("n", "K", vim.lsp.buf.hover, "Hover documentation")
                bufmap("n", "<leader>rn", vim.lsp.buf.rename, "Rename symbol")
                bufmap("n", "<leader>ca", vim.lsp.buf.code_action, "Code action")
                bufmap("n", "<leader>sr", telescope_builtin.lsp_references, "Search references")
                bufmap("n", "<leader>sd", function()
                    telescope_builtin.diagnostics({ bufnr = 0 })
                end, "Search diagnostics")
                bufmap("n", "<leader>f", function()
                    vim.lsp.buf.format({ async = true })
                end, "Format buffer")
            end

            local servers = {
                basedpyright = {
                    settings = {
                        basedpyright = {
                            analysis = {
                                typeCheckingMode = "basic",
                            },
                        },
                    },
                },
                ruff = {},
                clangd = {
                    cmd = {
                        "clangd",
                        "--background-index",
                        "--clang-tidy",
                        "--cross-file-rename",
                    },
                },
                ts_ls = {},
                eslint = {},
                terraformls = {},
                helm_ls = {
                    filetypes = { "helm" },
                },
                dockerls = {},
                verible = {},
                buf_ls = {},
                bashls = {},
                lua_ls = {
                    settings = {
                        Lua = {
                            diagnostics = {
                                globals = { "vim" },
                            },
                        },
                    },
                },
                jsonls = {},
                yamlls = {
                    settings = {
                        yaml = {
                            keyOrdering = false,
                        },
                    },
                },
                marksman = {},
            }
            for name, config in pairs(servers) do
                vim.lsp.config(name, vim.tbl_deep_extend("force", { on_attach = on_attach }, config))
            end
        end,
    },
    {
        "nvimtools/none-ls.nvim",
        dependencies = { "nvim-lua/plenary.nvim" },
        config = function()
            local null_ls = require("null-ls")

            local formatting = null_ls.builtins.formatting
            local diagnostics = null_ls.builtins.diagnostics
            local code_actions = null_ls.builtins.code_actions

            local sources = {
                -- C/C++
                formatting.clang_format,
                -- JavaScript/TypeScript
                formatting.prettier,
                -- Infrastructure
                formatting.terraform_fmt,
                diagnostics.terraform_validate,
                -- Verilog
                formatting.verible_verilog_format,
                -- Bash
                formatting.shfmt,
                formatting.shellharden,
                -- Lua
                formatting.stylua.with({
                    extra_args = { "--indent-type", "Spaces", "--indent-width", "4" },
                }),
                -- General
                code_actions.gitsigns,
            }

            null_ls.setup({ sources = sources })
        end,
    },
})
