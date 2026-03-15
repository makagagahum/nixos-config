{ config, pkgs, inputs, ... }: {
  # Bootloader
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  # CachyOS Kernel & Optimizations
  boot.kernelPackages = pkgs.linuxPackages_cachyos;
  chaotic.scx.enable = true; # High-performance scheduler
  
  networking.hostName = "x230";
  networking.networkmanager.enable = true;

  time.timeZone = "Asia/Manila";
  i18n.defaultLocale = "en_PH.UTF-8";

  # Graphics & Intel Hardware
  hardware.graphics = {
    enable = true;
    extraPackages = with pkgs; [
      intel-media-driver
      libva-intel-driver
      vulkan-intel
      intel-gpu-tools
    ];
  };

  # Sound
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    pulse.enable = true;
  };

  # User Configuration
  users.users.exorsus = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "video" "audio" ];
    shell = pkgs.zsh;
  };

  environment.systemPackages = with pkgs; [
    vim git wget curl pciutils usbutils fastfetch timeshift
  ];

  # Allow unfree packages (Chrome, etc.)
  nixpkgs.config.allowUnfree = true;

  system.stateVersion = "24.11";
}
