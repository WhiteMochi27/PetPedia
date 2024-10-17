{ pkgs }: {
    deps = [
      pkgs.libGLU
      pkgs.libGL
        pkgs.python310Full
        pkgs.python310Packages.pip
        pkgs.libglvnd
    ];
}

