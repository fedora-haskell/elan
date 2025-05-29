# workaround "Empty %files file BUILD/*/debugsourcefiles.list"
%define debug_package %{nil}

Name:           elan
Version:        4.1.2
Release:        1%{?dist}
Summary:        Lean4 version manager

License:        Apache-2.0
URL:            https://github.com/leanprover/elan
Source0:        https://github.com/leanprover/elan/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        elan-symlink-system-lean.sh

BuildRequires:  cargo
BuildRequires:  openssl-devel
# https://stackoverflow.com/questions/65553557/why-rust-is-failing-to-build-command-for-openssl-sys-v0-9-60-even-after-local-in
BuildRequires:  perl
# these are actually perl deps, but couldn't work out what other libs missing
BuildRequires:  perl-FindBin
BuildRequires:  perl-IPC-Cmd

%description
elan is a small tool for managing your installations of the Lean
theorem prover. It places lean and lake binaries in your PATH that
automatically select and, if necessary, download the Lean version
described in your project's lean-toolchain file. You can also install,
select, run, and uninstall Lean versions manually using the commands
of the elan executable.

%prep
%autosetup
# https://github.com/leanprover/elan/issues/168
sed -i -e 's/zip = "2.5.0"/zip = "3.0.0"/' Cargo.toml src/elan-dist/Cargo.toml

%build

%install
cargo install --path . --root %{buildroot}%{_prefix}
strip %{buildroot}%{_bindir}/elan-init
rm %{buildroot}%{_prefix}/.crates*

ln -s elan-init %{buildroot}%{_bindir}/elan

install %{SOURCE1} %{buildroot}%{_bindir}/elan-symlink-system-lean


%check
%{buildroot}%{_bindir}/elan --version | grep %{version}


%files
%license LICENSE
%{_bindir}/elan
%{_bindir}/elan-init
%{_bindir}/elan-symlink-system-lean


%changelog
* Thu May 29 2025 Jens Petersen <petersen@redhat.com> - 4.1.2-1
- https://github.com/leanprover/elan/blob/v4.1.2/CHANGELOG.md

* Mon Mar 03 2025 Jens Petersen  <petersen@redhat.com> - 4.0.0-1
- https://github.com/leanprover/elan/blob/v4.0.0/CHANGELOG.md
- elan-symlink-system-lean: default to system toolchain version

* Thu Nov 21 2024 Jens Petersen <petersen@redhat.com> - 3.1.1-2
- add elan-symlink-system-lean script

* Sun Jul 14 2024 Jens Petersen <petersen@redhat.com> - 3.1.1-1
- initial copr package
