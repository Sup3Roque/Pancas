import xbmc
import xbmcgui
import xbmcaddon
import os

ADDON        =  xbmcaddon.Addon(id='plugin.program.pancaswizard')
zip          =  ADDON.getSetting('zip')
d            =  xbmcgui.Dialog()

def CheckPath():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    print path
    try:
        os.makedirs(path)
        os.removedirs(path)
        d.ok('[COLOR=lime]SUCCESS[/COLOR]', 'Boas noticias. E possivel escrever neste caminho.', 'Algumas builds sao muitos grandes, nos recomendamos', '2Gb de espaco minimo disponivel.')
    except:
        d.ok('[COLOR=red]CANNOT WRITE TO PATH[/COLOR]', 'Nao e possivel escrever neste caminho. Por favor clique OK', 'nas definicoes para tentar de novo.', 'Alguns aparelhos geram resultados falsos, nos recomendamos usar uma pen USBcomo disco de backup.')

if __name__ == '__main__':
    CheckPath()