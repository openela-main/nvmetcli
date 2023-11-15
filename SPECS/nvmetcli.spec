Name:           nvmetcli
License:        ASL 2.0
Group:          Applications/System
Summary:        An adminstration shell for NVMe storage targets
Version:        0.7
Release:        5%{?dist}
URL:            ftp://ftp.infradead.org/pub/nvmetcli/
Source:         ftp://ftp.infradead.org/pub/nvmetcli/%{name}-%{version}.tar.gz
Patch0:         0001-Documentation-fix-typo.patch
Patch1:         0002-nvmetcli-don-t-remove-ANA-Group-1-on-clear.patch
Patch2:         0003-nvmetcli-set-up-the-target-only-after-the-network-is.patch
BuildArch:      noarch
BuildRequires:  python3-devel python3-setuptools systemd-units asciidoc xmlto
Requires:       python3-configshell python3-kmod
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains the command line interface to the NVMe over Fabrics
nvmet in the Linux kernel.  It allows configuring the nvmet interactively
as well as saving / restoring the configuration to / from a json file.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__python3} setup.py build
cd Documentation
make
gzip --stdout nvmetcli.8 > nvmetcli.8.gz

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/nvmet
install -m 644 nvmet.service %{buildroot}%{_unitdir}/nvmet.service
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 644 Documentation/nvmetcli.8.gz %{buildroot}%{_mandir}/man8/

%post
%systemd_post nvmet.service

%preun
%systemd_preun nvmet.service

%postun
%systemd_postun_with_restart nvmet.service

%files
%{python3_sitelib}/*
%dir %{_sysconfdir}/nvmet
%{_sbindir}/nvmetcli
%{_unitdir}/nvmet.service
%doc README
%license COPYING
%{_mandir}/man8/nvmetcli.8.gz

%changelog
* Tue Apr 04 2023 Maurizio Lombardi <mlombard@redhat.com> - 0.7-5
- Fix gating tests.

* Tue Apr 04 2023 Maurizio Lombardi <mlombard@redhat.com> - 0.7-4
- Fix BZ 2173777

* Wed Apr 28 2021 Maurizio Lombardi <mlombard@redhat.com> - 0.7-3
- Fix a failure when executing a clear command

* Thu Apr 22 2021 Maurizio Lombardi <mlombard@redhat.com> - 0.7-1
- Fix typo in the documentation

* Thu Apr 22 2021 Maurizio Lombardi <mlombard@redhat.com> - 0.7-1
- Update to the latest version

* Fri Sep 14 2018 Maurizio Lombardi <mlombard@redhat.com> - 0.6-2
- Support python3 dictionary access.

* Fri Jul 06 2018 Maurizio Lombardi <mlombard@redhat.com> - 0.6-1
- Update for new upstream release

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 9 2017 Andy Grover <agrover@redhat.com> - 0.4-1
- Update for new upstream release
- Remove fix-setup.patch

* Tue Feb 21 2017 Andy Grover <agrover@redhat.com> - 0.3-1
- Update for new upstream release

* Wed Oct 12 2016 Andy Grover <agrover@redhat.com> - 0.2-1
- Initial packaging
