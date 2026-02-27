Name:           harbour-dyncal
Version:        0.4.7
Release:        1
Summary:        DynCal - Dynamic Calendar Icon for Sailfish OS
Group:          System/Tools
Vendor:         fravaccaro
Distribution:   SailfishOS
Requires:       sailfish-version >= 5.0.0
Packager:       fravaccaro <fravaccaro@jollacommunity.it>
URL:            https://www.jollacommunity.it
License:        GPL-3.0-or-later

%description
DynCal changes the Calendar app icon dynamically based on the current day.

%prep
# No prep needed for this package

%build
# No build step required

%install
mkdir -p %{buildroot}/usr/share/harbour-dyncal
cp -r harbour-dyncal/usr/share/harbour-dyncal %{buildroot}/usr/share/harbour-dyncal

%files
%defattr(-,root,root,-)
/usr/share/harbour-dyncal/

%post
# Set executable permissions
chmod +x %{_datadir}/harbour-dyncal/*.sh

# Install systemd units
install -Dm644 %{_datadir}/harbour-dyncal/harbour-dyncal.service %{_sysconfdir}/systemd/system/harbour-dyncal.service
install -Dm644 %{_datadir}/harbour-dyncal/harbour-dyncal.timer %{_sysconfdir}/systemd/system/harbour-dyncal.timer

# Backup original calendar desktop file
cp /usr/share/applications/jolla-calendar.desktop %{_datadir}/harbour-dyncal/jolla-calendar.desktop.bak

# Run setup script
%{_datadir}/harbour-dyncal/harbour-dyncal.sh

# Enable and start systemd units
systemctl daemon-reload
systemctl enable --now harbour-dyncal.timer harbour-dyncal.service

%preun
# Run uninstall script
%{_datadir}/harbour-dyncal/harbour-dyncal-uninstall.sh

%postun
if [ $1 -eq 0 ]; then
    # Uninstall: Stop and disable services, remove files
    systemctl stop harbour-dyncal.timer harbour-dyncal.service 2>/dev/null || :
    systemctl disable harbour-dyncal.timer harbour-dyncal.service 2>/dev/null || :
    rm -f %{_sysconfdir}/systemd/system/harbour-dyncal.{service,timer}
    rm -rf %{_datadir}/harbour-dyncal
elif [ $1 -eq 1 ]; then
    # Upgrade: Re-run setup script
    %{_datadir}/harbour-dyncal/harbour-dyncal.sh
fi

%changelog
* Sat Oct 6 2018 - 0.4.6
- Bug fix.

* Mon Jul 3 2017 - 0.4.5
- Bug fix.

* Thu Jan 5 2017 - 0.4.4
- Bug fix.

* Thu Oct 6 2016 - 0.4.3
- Black icon fixed.

* Sat Sep 24 2016 - 0.4.2
- Icon jumping to the bottom of the app tray may be fixed.

* Wed Sep 21 2016 - 0.4.1
- High-res icons.
- Some icons redesigned.

* Tue Jan 19 2016 - 0.4.0
- Sailfish OS 2.0.7 support.

* Tue Dec 29 2015 - 0.3.1
- Reduced package size.

* Tue Dec 8 2015 - 0.3.0
- Extensions support added.

* Thu Oct 8 2015 - 0.2.5
- Holidays' icons updated.

* Wed Oct 7 2015 - 0.2.4
- Icon jumping to the bottom of the app tray may be fixed.

* Sat Oct 3 2015 - 0.2.3
- Bugfix.

* Tue Sep 29 2015 - 0.2.2
- Bugfix.

* Tue Sep 29 2015 - 0.2.1
- Bugfix.

* Mon Sep 28 2015 - 0.2
- Added some holidays' icons.
- Fixed icon not updating.

* Thu Sep 22 2015 - 0.1
- First build.
