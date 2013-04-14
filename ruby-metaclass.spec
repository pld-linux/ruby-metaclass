#
# Conditional build:
%bcond_without	tests		# build without tests

%define	gem_name metaclass
Summary:	Adds a metaclass method to all Ruby objects
Name:		ruby-%{gem_name}
Version:	0.0.1
Release:	1
Group:		Development/Languages
# https://github.com/floehopper/metaclass/issues/1
License:	MIT
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	563290373717a06691561ed1b5786a1b
URL:		http://github.com/floehopper/metaclass
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-minitest
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Adds a metaclass method to all Ruby objects

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version}

# test_helper.rb currently references bundler, so it is easier to avoid
# its usage at all.
sed -i '1,1d' test/object_methods_test.rb

%build
%if %{with tests}
RUBYOPT="-Ilib -rmetaclass" testrb test/object_methods_test.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{ruby_vendorlibdir}/metaclass.rb
%{ruby_vendorlibdir}/metaclass
