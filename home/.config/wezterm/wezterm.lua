local wezterm = require 'wezterm'
local act = wezterm.action

local config = wezterm.config_builder()

config.font = wezterm.font_with_fallback {
  'JetBrainsMono Nerd Font',
  'Hack Nerd Font',
  'JetBrains Mono',
  'Menlo',
}
config.font_size = 14
config.line_height = 1.08

-- same scheme as Ghostty, so both terminals match
config.color_scheme = 'rose-pine-moon'

config.window_decorations = 'RESIZE'
-- matched to Ghostty (0.8 / blur 50)
config.window_background_opacity = 0.8
config.macos_window_background_blur = 50
config.window_padding = {
  left = 14,
  right = 14,
  top = 12,
  bottom = 12,
}

config.use_fancy_tab_bar = false
config.hide_tab_bar_if_only_one_tab = true
config.tab_bar_at_bottom = true
config.scrollback_lines = 10000
config.audible_bell = 'Disabled'


-- Devin: pick any model from your Devin subscription and open it in a new tab.
-- LEADER (Ctrl+A) then d. The list comes live from `devin models`.
local DEVIN = os.getenv('HOME') .. '/.local/bin/devin'

local function devin_models()
  local ok, out = wezterm.run_child_process { DEVIN, 'models' }
  local choices = {}
  if not ok then
    return { { id = '', label = 'Could not read `devin models` (run `devin auth login`)' } }
  end
  local family = ''
  for line in out:gmatch('[^\n]+') do
    local fam = line:match('^(%S.-) %(')
    if fam then family = fam end
    local id, rest = line:match('^  ([%w][%w%.%-]+)%s%s%s+(.*)$')
    if id then
      table.insert(choices, { id = id, label = id .. '   ' .. rest })
    end
  end
  table.insert(choices, 1, { id = 'default', label = 'default   (Devin picks the model)' })
  return choices
end

local pick_devin_model = wezterm.action_callback(function(window, pane)
  window:perform_action(
    act.InputSelector {
      title = 'Devin model',
      fuzzy = true,
      fuzzy_description = 'Devin model: ',
      choices = devin_models(),
      action = wezterm.action_callback(function(win, p, id, label)
        if not id or id == '' then return end
        local args = { '/bin/zsh', '-lic', DEVIN .. (id == 'default' and '' or (' --model ' .. id)) }
        win:perform_action(act.SpawnCommandInNewTab { args = args, cwd = p:get_current_working_dir() and p:get_current_working_dir().file_path or nil }, p)
      end),
    },
    pane
  )
end)

config.launch_menu = {
  { label = 'Devin (default model)', args = { '/bin/zsh', '-lic', DEVIN } },
  { label = 'Devin SWE-2 Max', args = { '/bin/zsh', '-lic', DEVIN .. ' --model swe-2-max' } },
  { label = 'Devin Claude Opus 5.5', args = { '/bin/zsh', '-lic', DEVIN .. ' --model claude-opus-5.5' } },
  { label = 'Devin GPT-6.1 Sol', args = { '/bin/zsh', '-lic', DEVIN .. ' --model gpt-6.1-sol' } },
}

config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }
config.keys = {
  {
    key = '|',
    mods = 'LEADER|SHIFT',
    action = act.SplitHorizontal { domain = 'CurrentPaneDomain' },
  },
  {
    key = '-',
    mods = 'LEADER',
    action = act.SplitVertical { domain = 'CurrentPaneDomain' },
  },
  { key = 'h', mods = 'LEADER', action = act.ActivatePaneDirection 'Left' },
  { key = 'j', mods = 'LEADER', action = act.ActivatePaneDirection 'Down' },
  { key = 'k', mods = 'LEADER', action = act.ActivatePaneDirection 'Up' },
  { key = 'l', mods = 'LEADER', action = act.ActivatePaneDirection 'Right' },
  { key = 'z', mods = 'LEADER', action = act.TogglePaneZoomState },
  { key = 'c', mods = 'LEADER', action = act.SpawnTab 'CurrentPaneDomain' },
  { key = 'd', mods = 'LEADER', action = pick_devin_model },
  { key = 'Space', mods = 'LEADER', action = act.ShowLauncherArgs { flags = 'FUZZY|LAUNCH_MENU_ITEMS' } },
  {
    key = 'a',
    mods = 'LEADER|CTRL',
    action = act.SendKey { key = 'a', mods = 'CTRL' },
  },
}

return config
