{ config, pkgs, ... }: {
  home.username = "exorsus";
  home.homeDirectory = "/home/exorsus";
  home.stateVersion = "24.11";

  # User Packages
  home.packages = with pkgs; [
    qutebrowser
    firefox
    google-chrome
    thunar
    geany
    kitty
    alacritty
    grim
    slurp
    swappy
    wl-clipboard
    mako
    waybar
    rofi-wayland
    zsh
    oh-my-zsh
  ];

  # Managed Dotfiles (Symlink the current newm config)
  home.file.".config/newm/config.py".source = ./dotfiles/newm/config.py;

  # Programs settings
  programs.git = {
    enable = true;
    userName = "exorsus";
    userEmail = "exorsus@nixos.local";
  };

  # Auto-Sync script
  home.file."nixos-config/sync.sh" = {
    executable = true;
    text = ''
      #!/bin/bash
      cd ~/nixos-config
      git add .
      git commit -m "Auto-sync: $(date)"
      git push origin master
    '';
  };
}
