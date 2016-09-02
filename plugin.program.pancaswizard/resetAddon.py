#
#      Copyright (C) 2014 Richard Dean
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

plugin.program.psychowiz xbmc
plugin.program.psychowiz xbmcgui
plugin.program.psychowiz xbmcaddon
plugin.program.psychowiz shutil


def resetAddon():
    path = xbmc.translatePath('special://profile/addon_data/plugin.program.pancaswizard')
    shutil.rmtree(path)
    
    d = xbmcgui.Dialog()
    d.ok('[COLOR red][R][/COLOR][COLOR white]Pancas Team[/COLOR]', 'Community builds addon_data now removed.', 'Your locally stored builds will be unaffected but your', 'settings have now reset back to the defaults.')


if __name__ == '__main__':
    resetAddon()
