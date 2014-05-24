#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''
gui for SQLmap
'''
from Tkinter import *
import ttk
import os
import subprocess
import re
from urlparse import urlparse
import tkFont, tkFileDialog


class app(Frame):
    def __init__(self, mw):
        Frame.__init__(self, mw)
        self.grid( sticky='nswe' )
        # Hot Keys: ######################################
        mw.bind('<F1>',self.Help_F1)
        mw.bind('<Alt-Key-s>',self.alt_key_s)
        mw.bind('<Alt-Key-l>',self.alt_key_l)
        mw.bind('<Alt-Key-e>',self.alt_key_e)
        mw.bind('<F2>',self.commands)
        mw.bind('<Shift-Key-F2>',self.injectIT)
        mw.bind('<Button-3>',self.rClicker, add='')
        mw.bind('<Alt-Key-1>',self.alt_key_1)
        mw.bind('<Alt-Key-2>',self.alt_key_2)
        mw.bind('<Alt-Key-3>',self.alt_key_3)
        mw.bind('<Alt-Key-4>',self.alt_key_4)
        mw.bind('<Alt-Key-5>',self.alt_key_5)
        # ################################################
        self.rowconfigure( 0, weight=1 )
        self.columnconfigure( 0, weight=1 )
        self.nRoot = ttk.Notebook(self)
        BuilderFrame = ttk.Frame(self.nRoot)
        WatchLog = ttk.Frame(self.nRoot)
        Editor = ttk.Frame(self.nRoot)
        HelpMe = ttk.Frame(self.nRoot)
        self.nRoot.add(BuilderFrame, text=u'SQLmap 命令行构建')
        self.nRoot.add(WatchLog, text=u'Log 查看器')
        self.nRoot.add(Editor, text=u'编辑器')
        self.nRoot.add(HelpMe, text=u'帮助!')
        self.nRoot.rowconfigure( 0, weight=1 )
        self.nRoot.columnconfigure( 0, weight=1 )
        self.nRoot.grid(row=0, column=0, sticky='nswe',ipady=3,ipadx=3)
        BuilderFrame.rowconfigure( 0, weight=1 )
        BuilderFrame.columnconfigure( 0, weight=1)
        Editor.rowconfigure( 0, weight=1 )
        Editor.columnconfigure( 0, weight=1)
        HelpMe.rowconfigure( 0, weight=1 )
        HelpMe.columnconfigure( 0, weight=1)
        # Help SqlMAP
        lfhelp = ttk.Labelframe(HelpMe)
        lfhelp.grid(sticky='nswe')
        scrolHelp = ttk.Scrollbar(lfhelp)
        scrolHelp.grid(row=0, column=1, sticky='ns')
        lfhelp.rowconfigure( 0, weight=1 )
        lfhelp.columnconfigure( 0, weight=1)

        manual_sqlmap = 'python2 sqlmap.py -hh'
        process = subprocess.Popen(manual_sqlmap, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        helpTXT = Text(lfhelp, yscrollcommand=scrolHelp.set, width = 73,
                       height=24,bg='#002B36', fg='#93A1A1')
        helpTXT.insert('1.0', process.communicate()[0])
        scrolHelp.config(command= helpTXT.yview)
        helpTXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
        # EDITOR
        requestLF = ttk.Labelframe(Editor, text='')
        requestLF.grid(row = 0, column =0,sticky='nswe')
        requestLF.columnconfigure(0, weight=1)
        requestLF.rowconfigure(0, weight=1)
        #Open
        #Button Panel
        rbutPanel = ttk.Labelframe(Editor, text='')
        rbutPanel.grid(row=1, sticky='we',columnspan=2)
        rOpen = ttk.Button(rbutPanel, width=15)
        rOpen.config(text ="openReqFile", command=self.openReqF)
        rOpen.grid(row =1, column=0, sticky='w')
        cOpen = ttk.Button(rbutPanel, width=15)
        cOpen.config(text ="openConfFile", command=self.openIniF)
        cOpen.grid(row =1, column=1, sticky='w')
        rSave = ttk.Button(rbutPanel, width=15)
        rSave.config(text ="saveReqFile", command=self.saveReqF)
        rSave.grid(row =1, column=2, sticky='w')
        cSave = ttk.Button(rbutPanel, width=15)
        cSave.config(text ="saveConfFile", command=self.saveIniF)
        cSave.grid(row =1, column=3, sticky='w')
        self.file_request_save = save_request = {}
        save_request['defaultextension'] = '.txt'
        save_request['filetypes'] = [('all files', '.*')]
        save_request['initialdir'] = './SQM/REQUEST/'
        save_request['parent'] = Editor
        save_request['title'] = 'HTTP Requet FILE'
        self.file_ini = open_ini = {}
        open_ini['defaultextension'] = '.conf'
        open_ini['filetypes'] = [('all files', '.conf')]
        open_ini['initialdir'] = './SQM/CONFIGFILE/'
        open_ini['parent'] = Editor
        open_ini['title'] = 'CONFIGFILE'
        #
        reqFile_scr = ttk.Scrollbar(requestLF)
        reqFile_scr.grid(row=0, column=1, sticky='ns', columnspan=10)
        self.reqFile = Text(requestLF, yscrollcommand=reqFile_scr.set,undo=True, height=29, bg='#002B36', fg='#93A1A1')
        reqFile_scr.config(command= self.reqFile.yview)
        self.reqFile.grid(row=0, column=0,sticky='nswe')
        self.reqFile.columnconfigure(0, weight=1)
        self.reqFile.rowconfigure(0, weight=1)
        # Load Log...
        lfWatchLog = ttk.Labelframe(WatchLog, text='')
        WatchLog.rowconfigure( 0, weight=1 )
        WatchLog.columnconfigure( 0, weight=1)
        lfWatchLog.grid(row = 0, column =0, sticky='nswe', columnspan=10)
        lfWatchLog.rowconfigure( 0, weight=1 )
        lfWatchLog.columnconfigure( 0, weight=1)
        #
        scrolSes = ttk.Scrollbar(lfWatchLog)
        scrolSes.grid(row=0, column=1, sticky='ns')
        #
        self.sesTXT = Text(lfWatchLog, yscrollcommand=scrolSes.set, width = 73,
                           height=32,bg='#002B36', fg='#93A1A1')
        scrolSes.config(command= self.sesTXT.yview)
        self.sesTXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
        self.sesTXT.bind('<F3>',self.onFind)
        self.sesTXT.bind('<F4>',self.onFindAll)
        #Button Panel
        butPanel = ttk.Labelframe(WatchLog, text='')
        butPanel.grid(row=1, sticky='we',columnspan=2)
        logbut = ttk.Button(butPanel, width=3)
        logbut.config(text ="log", command=self.logs)
        logbut.grid(row =1, column=5, sticky='e')
        #full log
        self.chkLog = ttk.Checkbutton(butPanel)
        self.chkLog_var = StringVar()
        self.chkLog.config(text="full log", variable= self.chkLog_var, onvalue= "on" ,
                           offvalue = "off")#, command= self.chekLog)
        self.chkLog.grid(row=1,column = 4, sticky = 'e',padx=10)
        #
        sesbut = ttk.Button(butPanel, width=5)
        sesbut.config(text ="session", command=self.session)
        sesbut.grid(row =1, column=3,sticky='ws',ipadx=3)
        #
        self.search_var = StringVar()
        self.searchEdit = ttk.Entry(butPanel,width=30)
        self.searchEdit.config(text="", textvariable = self.search_var)
        self.searchEdit.grid(row=1, column=0, sticky = 'w', padx=3)
        self.search_var.set('HotKey: F3-find, F4-find all')
        self.searchEdit.bind('<F3>',self.onFind)
        self.searchEdit.bind('<F4>',self.onFindAll)
        self.sesTXT.bind('<Alt_L><r>',self.logs)
        #
        sesFbut = ttk.Button(butPanel, width=10)
        sesFbut.config(text ="open session", command=self.fSes)
        sesFbut.grid(row =1, column=6,sticky='ws',ipadx=3)
        self.file_session = options_session = {}
        options_session['defaultextension'] = ''
        options_session['filetypes'] = [('all files', '.*')]
        options_session['initialdir'] = './SQM/SESSION/'
        options_session['parent'] = WatchLog
        options_session['title'] = 'Open Session FILE'
        #
        trafbut = ttk.Button(butPanel, width=15)
        trafbut.config(text ="open traffic", command=self.fTraf)
        trafbut.grid(row =1, column=7,sticky='ws')
        self.file_traf = options_traf = {}
        options_traf['defaultextension'] = ''
        options_traf['filetypes'] = [('all files', '.*')]
        options_traf['initialdir'] = './SQM/TRAFFIC/'
        options_traf['parent'] = WatchLog
        options_traf['title'] = 'Open Traffic FILE'
        #
        panedUrl = ttk.Panedwindow(BuilderFrame, orient=VERTICAL)
        panedUrl.columnconfigure( 0, weight=1 )
        panedUrl.rowconfigure( 0, weight=1 )
        #TARGETS:
        targetVariant = ttk.Labelframe(panedUrl, text='')
        targetVariant.columnconfigure( 0, weight=1)
        panedUrl.add(targetVariant)
        #
        urlLF = ttk.Labelframe(panedUrl, text=u'目标:')
        urlLF.columnconfigure( 0, weight=1)
        urlLF.columnconfigure( 0, weight=1 )
        panedUrl.add(urlLF)
        #
        self.varTarget= StringVar()
        rbURL= ttk.Radiobutton(targetVariant,text='url',variable=self.varTarget,value="url", command=self.fTarget)
        rbLOG = ttk.Radiobutton(targetVariant,text='logFile',variable=self.varTarget,value="logFile", command=self.fTarget)
        rbBULKFILE =ttk.Radiobutton(targetVariant,text='bulkFile',variable=self.varTarget,value="bulkFile", command=self.fTarget)
        rbREQUEST =ttk.Radiobutton(targetVariant,text='请求文件',variable=self.varTarget,value="requestFile", command=self.fTarget)
        rbDork = ttk.Radiobutton(targetVariant,text='googleDork',variable=self.varTarget,value="googleDork", command=self.fTarget)
        rbDirect = ttk.Radiobutton(targetVariant,text='直接连接',variable=self.varTarget,value="direct", command=self.fTarget)
        rbConfig = ttk.Radiobutton(targetVariant,text='配置文件',variable=self.varTarget,value="configFile", command=self.fTarget)
        rbURL.grid(row=0, column=0,sticky='w')
        rbLOG.grid(row=0, column=1,sticky='w')
        rbBULKFILE.grid(row=0, column=2,sticky='w')
        rbREQUEST.grid(row=0, column=3,sticky='w')
        rbDork.grid(row=0, column=4,sticky='w')
        rbDirect.grid(row=0, column=5,sticky='w')
        rbConfig.grid(row=0, column=6,sticky='w')

        self.urlentry = ttk.Combobox(urlLF)
        self.urlentry.grid(row=1, column=0,sticky = 'we')
        texturl = open(r"./SQM/last.uri", 'a+').readlines()
        self.urlentry['values'] = texturl
        #query to sqlmap
        queryLF = ttk.Labelframe(panedUrl, text=u'sqlmap命令:')
        queryLF.columnconfigure( 0, weight=1 )
        queryLF.rowconfigure( 0, weight=1 )
        panedUrl.add(queryLF)
        self.sql_var = StringVar()
        self.sqlEdit = ttk.Entry(queryLF)
        self.sqlEdit.config(text="", textvariable = self.sql_var)
        self.sqlEdit.grid(sticky = 'we')
        self.sqlEdit.columnconfigure(0, weight=1)
        panedUrl.grid(row=0, column=0, sticky='nwe', rowspan =2)
        self.noBF = ttk.Notebook(BuilderFrame)
        setingsF = ttk.Frame(self.noBF)
        sDetTechF = ttk.Frame(self.noBF)
        requestF = ttk.Frame(self.noBF)
        enumerationF = ttk.Frame(self.noBF)
        fileF = ttk.Frame(self.noBF)
        self.noBF.add(setingsF, text='设置')
        self.noBF.add(sDetTechF, text='注入 | 探测 | 技术')
        self.noBF.add(requestF, text='Request')
        self.noBF.add(enumerationF, text='Enumeration')
        self.noBF.add(fileF, text='Access')
        self.noBF.columnconfigure(0, weight=1)
        self.noBF.grid(sticky = 'nswe',padx=3,pady=3)
        self.noBF.select(tab_id=1)

        setingsF.columnconfigure(0, weight=1)
        sDetTechF.columnconfigure(0, weight=1)
        requestF.columnconfigure(0, weight=1)
        fileF.columnconfigure(0, weight=1)
        # take query SqlMAP
        but = ttk.Button(BuilderFrame)
        but.config(text ="get query",width = 10, command=self.commands)
        #
        but.grid(row=3,column=0, sticky='nw')
        #
        butInj = ttk.Button(BuilderFrame)
        butInj.config(text ="start",width = 10, command=self.injectIT)
        butInj.grid(row=3,column=0, sticky='ne')
        #General:
        #These options can be used to set some general working parameters
        genOptLF = ttk.Labelframe(setingsF, text='General')
        genOptLF.grid(row=2, sticky='we',columnspan=2,pady=10)
        #--forms             Parse and test forms on target url
        self.chkForms = ttk.Checkbutton(genOptLF)
        self.chkForms_var = StringVar()
        self.chkForms.config(text="forms", variable= self.chkForms_var, onvalue= "on" ,
                             offvalue = "off", command= self.fForms)
        self.chkForms.grid(row=0,column=0,sticky = 'w')
        #--fresh-queries     Ignores query results stored in session file
        self.chkFresh = ttk.Checkbutton(genOptLF)
        self.chkFresh_var = StringVar()
        self.chkFresh.config(text="fresh-queries", variable= self.chkFresh_var, onvalue= "on" ,
                             offvalue = "off", command= self.fFresh)
        self.chkFresh.grid(row=1,column=0,sticky = 'w',ipadx=3)
        #--parse-errors      Parse and display DBMS error messages from responses
        self.chkParseEr = ttk.Checkbutton(genOptLF)
        self.chkParseEr_var = StringVar()
        self.chkParseEr.config(text="parse-errors", variable= self.chkParseEr_var, onvalue= "on" ,
                               offvalue = "off", command= self.chkParseEr)
        self.chkParseEr.grid(row=2,column=0,sticky = 'w')
        #--flush-session     Flush session file for current target
        self.chkFlush = ttk.Checkbutton(genOptLF)
        self.chkFlush_var = StringVar()
        self.chkFlush.config(text="flush-session", variable= self.chkFlush_var, onvalue= "on" ,
                             offvalue = "off", command= self.fFlush)
        self.chkFlush.grid(row=0,column=1,sticky = 'w',ipadx=3)
        #--replicate
        self.chkReplicate = ttk.Checkbutton(genOptLF)
        self.chkReplicate_var = StringVar()
        self.chkReplicate.config(text="replicate", variable= self.chkReplicate_var, onvalue= "on" ,
                                 offvalue = "off", command= self.fReplicate)
        self.chkReplicate.grid(row=1,column = 1, sticky = 'w')
        #--eta               Display for each output the estimated time of arrival
        self.chkEta = ttk.Checkbutton(genOptLF)
        self.chkEta_var = StringVar()
        self.chkEta.config(text="eta", variable= self.chkEta_var, onvalue= "on" ,
                           offvalue = "off", command= self.fEta)
        self.chkEta.grid(row=2,column=1,sticky = 'w')
        # Batch / Verbose OTHER
        self.chk_Batch = ttk.Checkbutton(genOptLF)
        self.chk_Batch_var = StringVar()
        self.chk_Batch.config(text="batch", variable= self.chk_Batch_var, onvalue= "on",
                              offvalue = "off", command= self.chekBatch)
        self.chk_Batch.grid(row=0,column=3, sticky= 'w',ipadx=3)
        # --hex
        self.chk_Hex = ttk.Checkbutton(genOptLF)
        self.chk_Hex_var = StringVar()
        self.chk_Hex.config(text="hex", variable= self.chk_Hex_var, onvalue= "on",
                            offvalue = "off", command= self.chekHex)
        self.chk_Hex.grid(row=1,column=3, sticky= 'w')
        #--save
        self.chk_Save = ttk.Checkbutton(genOptLF)
        self.chk_Save_var = StringVar()
        self.chk_Save.config(text="save", variable= self.chk_Save_var, onvalue= "on",
                             offvalue = "off", command= self.fSave)
        self.chk_Save.grid(row=2,column=3, sticky= 'w')
        #--charset=CHARSET   Force character encoding used for data retrieval
        self.chkCharset= ttk.Checkbutton(genOptLF)
        self.chkCharset_var = StringVar()
        self.chkCharset.config(text="charset", variable= self.chkCharset_var, onvalue= "on" ,
                               offvalue = "off", command= self.fCharset)
        self.chkCharset.grid(row=0,column=4,sticky = 'w')
        #
        self.eCharset = ttk.Entry(genOptLF,width=10)
        self.eCharset.grid(row=0,column=5, sticky='w',padx=3)
        #--crawl=CRAWLDEPTH  Crawl the website starting from the target url
        self.chkCrawl = ttk.Checkbutton(genOptLF)
        self.chkCrawl_var = StringVar()
        self.chkCrawl.config(text="crawl", variable= self.chkCrawl_var, onvalue= "on" ,
                             offvalue = "off", command= self.fCrawl)
        self.chkCrawl.grid(row=1,column=4,sticky = 'w')
        #
        self.eCrawl = ttk.Entry(genOptLF,width=15)
        self.eCrawl.grid(row=1,column=5, sticky='w',padx=3)
        #--csv-del=CSVDEL
        self.eCsv= ttk.Entry(genOptLF, width=15)
        self.eCsv.config(text="" , textvariable="" )
        self.eCsv.grid(row=2,column=5, sticky='w',padx=3)
        #
        self.chkCsv = ttk.Checkbutton(genOptLF)
        self.chkCsv_var = StringVar()
        self.chkCsv.config(text="csv-del", variable= self.chkCsv_var, onvalue= "on" ,
                           offvalue = "off", command= self.fCsv)
        self.chkCsv.grid(row=2,column = 4, sticky = 'w')
        #
        genFileLF = ttk.Labelframe(genOptLF, text='')
        genFileLF.grid(row=4, sticky='we',columnspan=10, rowspan=3)
        #-s SESSIONFILE      Save and resume all data retrieved on a session file
        self.chkSesFile = ttk.Checkbutton(genFileLF)
        self.chkSesFile_var = StringVar()
        self.chkSesFile.config(text="s SESSIONFILE", variable= self.chkSesFile_var, onvalue= "on" ,
                               offvalue = "off", command= self.fSesFile)
        self.chkSesFile.grid(row=0,column=0,sticky = 'w',ipadx=15)
        #
        self.eSesFile = ttk.Entry(genFileLF,width=20)
        self.eSesFile.grid(row=0,column=1, sticky='we')
        #-t TRAFFICFILE      Log all HTTP traffic into a textual file
        self.chkTrafFile = ttk.Checkbutton(genFileLF)
        self.chkTrafFile_var = StringVar()
        self.chkTrafFile.config(text="t TRAFFICFILE", variable= self.chkTrafFile_var, onvalue= "on" ,
                                offvalue = "off", command= self.fTrafFile)
        self.chkTrafFile.grid(row=1,column=0,sticky = 'w',ipadx=15)
        #
        self.eTrafFile = ttk.Entry(genFileLF,width=20)
        self.eTrafFile.grid(row=1,column=1, sticky='we')
        #
        #--output-dir=
        self.chkOutDir = ttk.Checkbutton(genFileLF)
        self.chkOutDir_var = StringVar()
        self.chkOutDir.config(text="output-dir", variable= self.chkOutDir_var, onvalue= "on" ,
                                offvalue = "off", command= self.fOutDir)
        self.chkOutDir.grid(row=0,column=3,sticky = 'w',ipadx=15)
        #
        self.eOutDir = ttk.Entry(genFileLF,width=20)
        self.eOutDir.grid(row=0,column=4, sticky='we')
        #--dbms-cred=DCRED
        self.chkDCRED = ttk.Checkbutton(genFileLF)
        self.chkDCRED_var = StringVar()
        self.chkDCRED.config(text="dbms-cred", variable= self.chkDCRED_var, onvalue= "on" ,
                             offvalue = "off", command= self.fDCRED)
        self.chkDCRED.grid(row=1,column=3,sticky = 'w',ipadx=15)
        #
        self.eDCRED = ttk.Entry(genFileLF,width=20)
        self.eDCRED.grid(row=1,column=4, sticky='we')
        # TOR
        #--check-tor         Check to see if Tor is used properly
        self.chkTor = ttk.Checkbutton(genOptLF)
        self.chkTor_var = StringVar()
        self.chkTor.config(text = "check-tor", variable= self.chkTor_var, onvalue= "on" ,
                           offvalue = "off", command= self.fTor)
        self.chkTor.grid(row=0,column=6, sticky='w')
        #--tor               Use Tor anonymity network
        self.chkTorUse = ttk.Checkbutton(genOptLF)
        self.chkTorUse_var = StringVar()
        self.chkTorUse.config(text = "use tor", variable= self.chkTorUse_var, onvalue= "on" ,
                              offvalue = "off", command= self.fTorUse)
        self.chkTorUse.grid(row=1,column=6,sticky='w')
        #--tor-port=TORPORT  Set Tor proxy port other than default
        self.chkTorPort = ttk.Checkbutton(genOptLF)
        self.chkTorPort_var = StringVar()
        self.chkTorPort.config(text="tor-port", variable= self.chkTorPort_var, onvalue= "on" ,
                               offvalue = "off", command= self.fTorPort)
        self.chkTorPort.grid(row=0,column=7,sticky = 'w')
        #
        self.eTorPort = ttk.Entry(genOptLF,width=6)
        self.eTorPort.grid(row=0,column=8, sticky='w')
        #--tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
        self.chkTorType = ttk.Checkbutton(genOptLF)
        self.chkTorType_var = StringVar()
        self.chkTorType.config(text="tor-type", variable= self.chkTorType_var, onvalue= "on" ,
                               offvalue = "off", command= self.fTorType)
        self.chkTorType.grid(row=1,column=7,sticky = 'w')
        #
        self.eTorType = ttk.Entry(genOptLF,width=6)
        self.eTorType.grid(row=1,column=8, sticky='w')
        #Miscellaneous:
        miscOptLF = ttk.Labelframe(setingsF, text='Miscellaneous')
        miscOptLF.grid(row=3, sticky='we',columnspan=2,pady=10)
        #--beep              Sound alert when SQL injection found
        self.chkBeep = ttk.Checkbutton(miscOptLF)
        self.chkBeep_var = StringVar()
        self.chkBeep.config(text = "beep", variable= self.chkBeep_var, onvalue= "on" ,
                           offvalue = "off", command= self.fBeep)
        self.chkBeep.grid(row=0,column=0, sticky='w',ipadx=10)
        #--check-payload     Offline WAF/IPS/IDS payload detection testing
        self.chkPayload = ttk.Checkbutton(miscOptLF)
        self.chkPayload_var = StringVar()
        self.chkPayload.config(text = "check-payload", variable= self.chkPayload_var, onvalue= "on" ,
                            offvalue = "off", command= self.fPayload)
        self.chkPayload.grid(row=1,column=0, sticky='w',ipadx=10)
        #--check-waf         Check for existence of WAF/IPS/IDS protection
        self.chkWaf = ttk.Checkbutton(miscOptLF)
        self.chkWaf_var = StringVar()
        self.chkWaf.config(text = "check-waf", variable= self.chkWaf_var, onvalue= "on" ,
                               offvalue = "off", command= self.fWaf)
        self.chkWaf.grid(row=2,column=0, sticky='w')
        #--cleanup           Clean up the DBMS by sqlmap specific UDF and tables
        self.chkCleanup = ttk.Checkbutton(miscOptLF)
        self.chkCleanup_var = StringVar()
        self.chkCleanup.config(text = "cleanup", variable= self.chkCleanup_var, onvalue= "on" ,
                               offvalue = "off", command= self.fCleanup)
        self.chkCleanup.grid(row=0,column=1, sticky='w')
        #--dependencies      Check for missing sqlmap dependencies
        self.chkDependencies = ttk.Checkbutton(miscOptLF)
        self.chkDependencies_var = StringVar()
        self.chkDependencies.config(text = "dependencies", variable= self.chkDependencies_var, onvalue= "on" ,
                               offvalue = "off", command= self.fDependencies)
        self.chkDependencies.grid(row=1,column=1, sticky='w',ipadx=10)
        #--mobile            Imitate smartphone through HTTP User-Agent header
        self.chkMobile = ttk.Checkbutton(miscOptLF)
        self.chkMobile_var = StringVar()
        self.chkMobile.config(text = "mobile", variable= self.chkMobile_var, onvalue= "on" ,
                                    offvalue = "off", command= self.fMobile)
        self.chkMobile.grid(row=2,column=1, sticky='w')
        #--page-rank         Display page rank (PR) for Google dork results
        self.chkRank = ttk.Checkbutton(miscOptLF)
        self.chkRank_var = StringVar()
        self.chkRank.config(text = "page-rank", variable= self.chkRank_var, onvalue= "on" ,
                                    offvalue = "off", command= self.fRank)
        self.chkRank.grid(row=0,column=2, sticky='w')
        #--purge-output      Safely remove all content from output directory
        self.chkPurge = ttk.Checkbutton(miscOptLF)
        self.chkPurge_var = StringVar()
        self.chkPurge.config(text = "purge-output", variable= self.chkPurge_var, onvalue= "on" ,
                                    offvalue = "off", command= self.fPurge)
        self.chkPurge.grid(row=1,column=2, sticky='w',ipadx=10)
        #--smart             Conduct through tests only if positive heuristic(s)
        self.chkSmart = ttk.Checkbutton(miscOptLF)
        self.chkSmart_var = StringVar()
        self.chkSmart.config(text = "smart", variable= self.chkSmart_var, onvalue= "on" ,
                                    offvalue = "off", command= self.fSmart)
        self.chkSmart.grid(row=2,column=2, sticky='w')
        #--gpage=GOOGLEPAGE  Use Google dork results from specified page number
        self.chkGpage = ttk.Checkbutton(miscOptLF)
        self.chkGpage_var = StringVar()
        self.chkGpage.config(text="gpage", variable= self.chkGpage_var, onvalue= "on" ,
                                offvalue = "off", command= self.fGpage)
        self.chkGpage.grid(row=0,column=3,sticky = 'w')
        #
        self.eGpage = ttk.Entry(miscOptLF,width=10)
        self.eGpage.grid(row=0,column=4, sticky='w', padx=5)
        # --test-filter=TSTF
        self.chkTSTF = ttk.Checkbutton(miscOptLF)
        self.chkTSTF_var = StringVar()
        self.chkTSTF.config(text="test-filter", variable= self.chkTSTF_var, onvalue= "on" ,
                            offvalue = "off", command= self.fTSTF)
        self.chkTSTF.grid(row=1,column=3,sticky = 'w')
        #
        self.eTSTF = ttk.Entry(miscOptLF,width=10)
        self.eTSTF.grid(row=1,column=4, sticky='w', padx=5)
        #--exact
        self.chkExact = ttk.Checkbutton(miscOptLF)
        self.chkExact_var = StringVar()
        self.chkExact.config(text = "exact", variable= self.chkExact_var, onvalue= "on" ,
                                    offvalue = "off", command= self.fExact)
        self.chkExact.grid(row=2,column=3, sticky='w')
        #--disable-hash      Disable password hash cracking mechanism
        self.chkDHash = ttk.Checkbutton(miscOptLF)
        self.chkDHash_var = StringVar()
        self.chkDHash.config(text = "disable-hash", variable= self.chkDHash_var, onvalue= "on" ,
                             offvalue = "off", command= self.fDHash)
        self.chkDHash.grid(row=0,column=5, sticky='w')
        #--disable-like      Disable LIKE search of identificator names
        self.chkDLike = ttk.Checkbutton(miscOptLF)
        self.chkDLike_var = StringVar()
        self.chkDLike.config(text = "disable-like", variable= self.chkDLike_var, onvalue= "on" ,
                             offvalue = "off", command= self.fDLike)
        self.chkDLike.grid(row=1,column=5, sticky='w')
        #
        optimiz_LF = ttk.Labelframe(setingsF, text='Optimizations, Fingerprint, Verbose')
        optimiz_LF.grid(row=0, sticky='we', pady=10,columnspan=4)
        optimiz_LF.columnconfigure(0, weight=1)
        #
        self.chkOpt = ttk.Checkbutton(optimiz_LF)
        self.chkOpt_var = StringVar()
        self.chkOpt.config(text="o", variable= self.chkOpt_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekOpt)
        self.chkOpt.grid(row=0,column = 0, sticky = 'wn', pady=1)
        #-ALL
        self.chkO = ttk.Checkbutton(optimiz_LF)
        self.chkO_var = StringVar()
        self.chkO.config(text="o", variable= self.chkO_var, onvalue= "on" ,
                            offvalue = "off", command= self.fO)
        self.chkO.grid(row=0,column = 0, sticky = 'w')
        #--predict-output    Predict common queries output
        self.chkPred = ttk.Checkbutton(optimiz_LF)
        self.chkPred_var = StringVar()
        self.chkPred.config(text="predict-output", variable= self.chkPred_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekPred)
        self.chkPred.grid(row=0,column = 1, sticky = 'w')
        #--keep-alive
        self.chkKeep = ttk.Checkbutton(optimiz_LF)
        self.chkKeep_var = StringVar()
        self.chkKeep.config(text="keep-alive", variable= self.chkKeep_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekKeep)
        self.chkKeep.grid(row=0,column = 3, sticky = 'w')
        #--null-connection   Retrieve page length without actual HTTP response body
        self.chkNull = ttk.Checkbutton(optimiz_LF)
        self.chkNull_var = StringVar()
        self.chkNull.config(text="null-connection", variable= self.chkNull_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekNull)
        self.chkNull.grid(row=0,column = 4, sticky = 'w')
        #--threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
        self.chk_thr = ttk.Checkbutton(optimiz_LF)
        self.chk_thr_var = StringVar()
        self.chk_thr.config(text="threads", variable= self.chk_thr_var, onvalue= "on",
                            offvalue = "off", command= self.chek_thr)
        self.chk_thr.grid(row=0,column=5,sticky = 'w')
        self.thr = ttk.Combobox(optimiz_LF)
        self.thr_value = StringVar()
        self.thr.config(textvariable=self.thr_value, state='disable', width = 2)
        self.thr['values'] = ('1','2', '3','4','5','6','7','8','9','10')
        self.thr.current(0)
        self.thr.bind('<<ComboboxSelected>>', self.chek_thr)
        self.thr.grid(row=0,column=6,sticky ='w',padx=5)
        #-f, --fingerprint
        self.chk_fing = ttk.Checkbutton(optimiz_LF)
        self.chk_fing_var = StringVar()
        self.chk_fing.config(text="fingerprint", variable= self.chk_fing_var, onvalue= "on",
                             offvalue = "off", command= self.chekFing)
        self.chk_fing.grid(row=0,column=7, sticky= 'w')
        # Verbose
        self.chk_verb = ttk.Checkbutton(optimiz_LF)
        self.chk_verb_var = StringVar()
        self.chk_verb.config(text="verbose", variable= self.chk_verb_var, onvalue= "on",
                             offvalue = "off", command= self.chek_verb)
        self.chk_verb.grid(row=0,column=8, sticky='w')
        self.box_verb = ttk.Combobox(optimiz_LF)
        self.box_verb_value = StringVar()
        self.box_verb.config(textvariable=self.box_verb_value, state='disabled', width = 2)
        self.box_verb['values'] = ('0','1', '2', '3','4','5','6')
        self.box_verb.current(0)
        self.box_verb.bind('<<ComboboxSelected>>', self.chek_verb)
        self.box_verb.grid(row=0,column=9,sticky ='w')
        # Group (Injection, Detections,Techniques)
        panedITO = ttk.Panedwindow(sDetTechF, orient=HORIZONTAL)
        panedITO.rowconfigure( 0, weight=1 )
        panedITO.columnconfigure( 0, weight=1 )
        #
        injectionLF = ttk.Labelframe(panedITO, text='Injection')
        injectionLF.rowconfigure(0, weight=1 )
        injectionLF.columnconfigure( 0, weight=1 )
        #
        tampersLF = ttk.Labelframe(panedITO, text='Tampers')
        tampersLF.rowconfigure( 0, weight=1 )
        tampersLF.columnconfigure( 0, weight=1 )
        #
        panedITO.add(injectionLF)
        panedITO.add(tampersLF)
        panedITO.grid(row=0, column=0,pady=10, sticky='we')
        #
        #-p TESTPARAMETER    Testable parameter(s)
        self.entryParam = ttk.Entry(injectionLF)
        self.entryParam.config(width=30)
        self.entryParam.grid(row=3,column=1, sticky='we',padx=3)
        #
        self.chkParam = ttk.Checkbutton(injectionLF)
        self.chkParam_var = StringVar()
        self.chkParam.config(text="parametr", variable= self.chkParam_var, onvalue= "on" ,
                             offvalue = "off", command= self.chekParam)
        self.chkParam.grid(row=3,column = 0, sticky = 'w')
        # Select database
        self.chk_dbms = ttk.Checkbutton(injectionLF)
        self.chk_dbms_var = StringVar()
        self.chk_dbms.config(text="dbms", variable= self.chk_dbms_var, onvalue= "on" ,
                             offvalue = "off", command= self.chek_dbms)
        self.chk_dbms.grid(row=0,column=0,sticky = 'sw')
        #
        self.box = ttk.Combobox(injectionLF)
        self.box_value = StringVar()
        self.box.config(textvariable=self.box_value, state='disabled', width = 30)
        self.box['values'] = ("access", "db2", "firebird", "maxdb", "mssqlserver", "mysql", "oracle", "postgresql", "sqlite", "sybase")
        self.box.current(0)
        self.box.bind('<<ComboboxSelected>>', self.chek_dbms)
        self.box.grid(row=0,column=1,sticky ='sw',padx=3)
        # Prefix:
        self.entryPrefix = ttk.Entry(injectionLF)
        self.entryPrefix.config(text="" , textvariable="", width = 30)
        self.entryPrefix.grid(row=4,column=1, sticky='we',padx=3)
        #
        self.chkPrefix = ttk.Checkbutton(injectionLF)
        self.chkPrefix_var = StringVar()
        self.chkPrefix.config(text="prefix", variable= self.chkPrefix_var, onvalue= "on" ,
                              offvalue = "off", command= self.chekPrefix)
        self.chkPrefix.grid(row=4,column = 0, sticky = W)
        # Suffix:
        self.entrySuffix = ttk.Entry(injectionLF)
        self.entrySuffix.config(text="" , textvariable="", width = 30)
        self.entrySuffix.grid(row=5,column=1, sticky='we',padx=3)
        #
        self.chkSuffix = ttk.Checkbutton(injectionLF)
        self.chkSuffix_var = StringVar()
        self.chkSuffix.config(text="suffix", variable= self.chkSuffix_var, onvalue= "on" ,
                              offvalue = "off", command= self.chekSuffix)
        self.chkSuffix.grid(row=5,column = 0, sticky = 'w')
        # --os
        self.entryOS = ttk.Entry(injectionLF)
        self.entryOS.config(text="" , textvariable="", width = 30)
        self.entryOS.grid(row=6,column=1, sticky='we',padx=3)
        #
        self.chkOS = ttk.Checkbutton(injectionLF)
        self.chkOS_var = StringVar()
        self.chkOS.config(text="OS", variable= self.chkOS_var, onvalue= "on" ,
                          offvalue = "off", command= self.chekOS)
        self.chkOS.grid(row=6,column = 0, sticky = 'w')
        #--skip
        self.entrySkip = ttk.Entry(injectionLF)
        self.entrySkip.config(text="" , textvariable="", width = 30)
        self.entrySkip.grid(row=7,column=1, sticky='we',padx=3)
        #
        self.chkSkip = ttk.Checkbutton(injectionLF)
        self.chkSkip_var = StringVar()
        self.chkSkip.config(text="skip", variable= self.chkSkip_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekSkip)
        self.chkSkip.grid(row=7,column = 0, sticky = 'w')
        #
        panedInj = ttk.Panedwindow(injectionLF, orient=HORIZONTAL)
        panedInj.rowconfigure( 0, weight=1 )
        panedInj.columnconfigure( 0, weight=1 )
        #add:
        chkInjLF = ttk.Labelframe(panedInj, text='')
        chkInjLF.rowconfigure( 0, weight=1 )
        chkInjLF.columnconfigure( 0, weight=1 )
        #
        panedInj.add(chkInjLF)
        panedInj.grid(row=8, column=0,columnspan=2, sticky='we')
        #--invalid-logical
        self.chkLogical = ttk.Checkbutton(chkInjLF)
        self.chkLogical_var = StringVar()
        self.chkLogical.config(text="invalid-logical", variable= self.chkLogical_var, onvalue= "on" ,
                               offvalue = "off", command= self.chekLogical,width=14)
        self.chkLogical.grid(row=0,column=0,sticky = 'w')
        #--invalid-bignum
        self.chkBigNum = ttk.Checkbutton(chkInjLF)
        self.chkBigNum_var = StringVar()
        self.chkBigNum.config(text="invalid-bignum", variable= self.chkBigNum_var, onvalue= "on" ,
                              offvalue = "off", command= self.chekBigNum,width=14)
        self.chkBigNum.grid(row=0,column=1,sticky = 'w')
        #--no-cast
        self.chkCast = ttk.Checkbutton(chkInjLF)
        self.chkCast_var = StringVar()
        self.chkCast.config(text="no-cast", variable= self.chkCast_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekCast)
        self.chkCast.grid(row=0,column=2,sticky = 'w')
        #-Tamper:
        self.Ltamper=Listbox(tampersLF,height=8,width=25,selectmode=EXTENDED)
        # *.py in listbox, exclude __init__.py
        files_tamper = os.listdir('./tamper')
        tampers = filter(lambda x: x.endswith('.py'), files_tamper)
        for tamp_list in sorted(tampers):
            if tamp_list not in "__init__.py":
                self.Ltamper.insert(END,tamp_list)
        self.Ltamper.rowconfigure( 0, weight=1 )
        self.Ltamper.columnconfigure( 0, weight=1 )
        self.Ltamper.grid(row =0, column = 0, padx=5, sticky='nswe')
        # Tamper Scroll
        scrollTamper = ttk.Scrollbar(tampersLF, orient=VERTICAL, command=self.Ltamper.yview)
        self.Ltamper['yscrollcommand'] = scrollTamper.set
        scrollTamper.grid(row=0,column=1, sticky='ns')
        #
        panedDTO = ttk.Panedwindow(sDetTechF, orient=HORIZONTAL)
        panedDTO.columnconfigure( 0, weight=1 )
        #
        detectionLF = ttk.Labelframe(panedDTO, text='Detection')
        detectionLF.columnconfigure( 0, weight=1 )
        #
        techniqueLF = ttk.Labelframe(panedDTO, text='Technique')
        techniqueLF.columnconfigure( 0, weight=1 )
        #
        panedDTO.add(detectionLF)
        panedDTO.add(techniqueLF)
        panedDTO.grid(row=1, column=0, columnspan=2,sticky='we',ipady=0)
        # String:
        self.entryStr = ttk.Entry(detectionLF,width=30)
        self.entryStr.grid(row=0,column=1, sticky = 'e',padx=3)
        #
        self.chkStr = ttk.Checkbutton(detectionLF)
        self.chkStr_var = StringVar()
        self.chkStr.config(text="String", variable= self.chkStr_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekStr)
        self.chkStr.grid(row=0,column = 0, sticky = 'sw',ipadx=16)
        #--regexp=REGEXP
        self.entryReg = ttk.Entry(detectionLF,width=30)
        self.entryReg.grid(row=1,column=1, sticky = 'we',padx=3)
        #
        self.chkReg = ttk.Checkbutton(detectionLF)
        self.chkReg_var = StringVar()
        self.chkReg.config(text="Regexp", variable= self.chkReg_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekReg)
        self.chkReg.grid(row=1,column = 0, sticky = 'w')
        #--code=CODE
        self.chkCode = ttk.Checkbutton(detectionLF)
        self.chkCode_var = StringVar()
        self.chkCode.config(text="Code", variable= self.chkCode_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekCode)
        self.chkCode.grid(row=3,column = 0, sticky = 'w')
        #
        self.entryCode = ttk.Entry(detectionLF,width=30)
        self.entryCode.grid(row=3,column=1, sticky = 'we',padx=3)
        #--level=LEVEL
        self.chk_level = ttk.Checkbutton(detectionLF)
        self.chk_level_var = StringVar()
        self.chk_level.config(text="level", variable= self.chk_level_var, onvalue= "on" ,
                              offvalue = "off", command= self.chek_level)
        self.chk_level.grid(row=4,column=0,sticky = 'w')
        #
        self.box_level = ttk.Combobox(detectionLF)
        self.box_level_value = StringVar()
        self.box_level.config(textvariable=self.box_level_value, state='disabled', width = 5)
        self.box_level['values'] = ('1', '2', '3','4','5')
        self.box_level.current(0)
        self.box_level.bind('<<ComboboxSelected>>', self.chek_level)
        self.box_level.grid(row=4,column=1,sticky = 'w',padx=3)
        #--risk=RISK
        self.chk_risk = ttk.Checkbutton(detectionLF)
        self.chk_risk_var = StringVar()
        self.chk_risk.config(text="risk", variable= self.chk_risk_var, onvalue= "on",
                             offvalue = "off", command= self.chek_risk)
        self.chk_risk.grid(row=5,column=0,sticky = 'w')
        #
        self.box_risk = ttk.Combobox(detectionLF)
        self.box_risk_value = StringVar()
        self.box_risk.config(textvariable=self.box_risk_value, state='disabled', width = 5)
        self.box_risk['values'] = ('1', '2', '3')
        self.box_risk.current(0)
        self.box_risk.bind('<<ComboboxSelected>>', self.chek_risk)
        self.box_risk.grid(row=5,column=1,sticky = 'w',padx=3)
        #--text-only
        self.chkTxt = ttk.Checkbutton(detectionLF)
        self.chk_Txt_var = StringVar()
        self.chkTxt.config(text="text-only", variable= self.chk_Txt_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekTxt)
        self.chkTxt.grid(row=6,column = 0, sticky = 'w')
        #--titles
        self.chkTit = ttk.Checkbutton(detectionLF)
        self.chk_Tit_var = StringVar()
        self.chkTit.config(text="titles", variable= self.chk_Tit_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekTit)
        self.chkTit.grid(row=7,column = 0, sticky = 'w')
        #--technique=TECH
        self.chk_tech = ttk.Checkbutton(techniqueLF)
        self.chk_tech_var = StringVar()
        self.chk_tech.config(text="technique", variable= self.chk_tech_var, onvalue= "on",
                             offvalue = "off", command= self.chek_tech)
        self.chk_tech.grid(row=0,column=0,sticky = 'nw')
        #
        self.boxInj = ttk.Combobox(techniqueLF)
        self.boxInj_value = StringVar()
        self.boxInj.config(textvariable=self.boxInj_value, state='disabled', width = 15)
        self.boxInj['values'] = ('B','E', 'U','S','T')
        self.boxInj.current(0)
        self.boxInj.bind('<<ComboboxSelected>>', self.chek_tech)
        self.boxInj.grid(row=0,column=1,sticky ='nwe',padx=3)
        #
        self.entryCol = ttk.Entry(techniqueLF)
        self.entryCol.config(text = "" , textvariable = "", width = 15)
        self.entryCol.grid(row = 1,column = 1, sticky='nwe',padx=3)
        #
        self.chkCol = ttk.Checkbutton(techniqueLF)
        self.chkCol_var = StringVar()
        self.chkCol.config(text="cols", variable= self.chkCol_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekCol)
        self.chkCol.grid(row=1,column = 0, sticky = 'nw')
        #--union-char
        self.entryChar = ttk.Entry(techniqueLF)
        self.entryChar.config(text="" , textvariable="", width = 15)
        self.entryChar.grid(row=2,column=1, sticky='nwe',padx=3)
        #
        self.chkChar = ttk.Checkbutton(techniqueLF)
        self.chkChar_var = StringVar()
        self.chkChar.config(text="char", variable= self.chkChar_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekChar)
        self.chkChar.grid(row=2,column = 0, sticky = 'nw')
        #--time-sec
        self.entrySec = ttk.Entry(techniqueLF)
        self.entrySec.config(text="" , textvariable="", width = 15)
        self.entrySec.grid(row=3,column=1, sticky='nwe',padx=3)
        #
        self.chkSec = ttk.Checkbutton(techniqueLF)
        self.chkSec_var = StringVar()
        self.chkSec.config(text="time-sec", variable= self.chkSec_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekSec)
        self.chkSec.grid(row=3,column = 0, sticky = 'nw')
        #
        self.entryDNS = ttk.Entry(techniqueLF)
        self.entryDNS.config(text="" , textvariable="", width = 15)
        self.entryDNS.grid(row=4,column=1, sticky='nwe',padx=3)
        #--dns-domain
        self.chkDNS = ttk.Checkbutton(techniqueLF)
        self.chkDNS_var = StringVar()
        self.chkDNS.config(text="dns-domain", variable= self.chkDNS_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekDNS)
        self.chkDNS.grid(row=4, column = 0, sticky = 'nw')
        sep = ttk.Separator(techniqueLF, orient=HORIZONTAL)
        sep.grid(row = 5, ipady=20, sticky='w')
        # data
        dataN = ttk.Notebook(requestF)
        data1 = ttk.Frame(dataN)
        dataN.add(data1, text='   1   ')
        data1.columnconfigure(0, weight=1)
        data2 = ttk.Frame(dataN)
        dataN.add(data2, text='   2   ')
        data2.columnconfigure(0, weight=1)
        dataN.columnconfigure(0, weight=1)
        dataN.grid(row=0,sticky = 'nswe',padx=5,pady=5)
        dataLF = ttk.Labelframe(data1, text='')
        dataLF.grid(row = 0, column =0,pady=10, sticky='we')
        #DATA 1
        #--random-agent
        self.chkRandomAg = ttk.Checkbutton(dataLF)
        self.chkRandomAg_var = StringVar()
        self.chkRandomAg.config(text = "random-agent", variable= self.chkRandomAg_var, onvalue= "on", offvalue = "off", command= self.fRandomAg)
        self.chkRandomAg.grid(row=0,column=0, sticky='w')
        #--data=DATA         Data string to be sent through POST
        self.chkdata = ttk.Checkbutton(dataLF)
        self.chkdata_var = StringVar()
        self.chkdata.config(text = "data", variable= self.chkdata_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekdata)
        self.chkdata.grid(row=1,column=0, sticky='w')
        #
        self.entryData = ttk.Entry(dataLF, width=60)
        self.entryData.grid(row =1,column=1, sticky='we',padx=3)
        self.entryData.columnconfigure(0, weight=1)
        #--param-del=PDEL
        self.chkPDEL = ttk.Checkbutton(dataLF)
        self.chkPDEL_var = StringVar()
        self.chkPDEL.config(text = "param-del", variable= self.chkPDEL_var, onvalue= "on" ,
                            offvalue = "off", command= self.fPDEL)
        self.chkPDEL.grid(row=2,column=0, sticky='w')
        #
        self.ePDEL = ttk.Entry(dataLF, width=60)
        self.ePDEL.grid(row =2,column=1, sticky='we',padx=3)
        self.ePDEL.columnconfigure(0, weight=1)
        #--cookie=COOKIE     HTTP Cookie header
        self.chkCook = ttk.Checkbutton(dataLF)
        self.chkCook_var = StringVar()
        self.chkCook.config(text="cookie", variable= self.chkCook_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekCook)
        self.chkCook.grid(row=3,column=0, sticky='w')
        self.entryCook = ttk.Entry(dataLF, width=60)
        self.entryCook.grid(row=3,column=1, sticky='we',padx=3)
        self.entryCook.columnconfigure(0, weight=1)
        #--load-cookies=LOC  File containing cookies in Netscape/wget format
        self.chkLoadCookies = ttk.Checkbutton(dataLF)
        self.chkLoadCookies_var = StringVar()
        self.chkLoadCookies.config(text="load-cookies", variable= self.chkLoadCookies_var, onvalue= "on" ,
                                   offvalue = "off", command= self.fLoadCookies)
        self.chkLoadCookies.grid(row=4,column=0, sticky='w')
        #
        self.varLoadCookies = StringVar()
        self.eLoadCookies = ttk.Entry(dataLF, width=60)
        self.eLoadCookies.config(text="", textvariable = self.varLoadCookies)
        self.eLoadCookies.grid(row=4,column=1, sticky='we',padx=3)
        self.eLoadCookies.columnconfigure(0, weight=1)
        #--cookie-urlencode  URL Encode generated cookie injections
        self.chkCookieUrlencode = ttk.Checkbutton(dataLF)
        self.chkCookieUrlencode_var = StringVar()
        self.chkCookieUrlencode.config(text="cookie-urlencode", variable= self.chkCookieUrlencode_var, onvalue= "on" ,
                                       offvalue = "off", command= self.fCookieUrlencode)
        self.chkCookieUrlencode.grid(row=5,column=0, sticky='w')
        #--drop-set-cookie
        self.chkDropSetCookie = ttk.Checkbutton(dataLF)
        self.chkDropSetCookie_var = StringVar()
        self.chkDropSetCookie.config(text="drop-set-cookie", variable= self.chkDropSetCookie_var, onvalue= "on" ,
                                     offvalue = "off", command= self.fDropSetCookie)
        self.chkDropSetCookie.grid(row=6,column=0, sticky='w')
        #--user-agent=AGENT  HTTP User-Agent header
        self.chkUA = ttk.Checkbutton(dataLF)
        self.chkUA_var = StringVar()
        self.chkUA.config(text="user-agent", variable= self.chkUA_var, onvalue= "on" ,
                          offvalue = "off", command= self.fUA)
        self.chkUA.grid(row=7,column=0, sticky='w')
        #
        self.eUA = ttk.Entry(dataLF, width=60)
        self.eUA.grid(row=7,column=1, sticky='we',padx=3)
        self.eUA.columnconfigure(0, weight=1)
        #--randomize=RPARAM  Randomly change value for given parameter(s)
        self.chkRandomize = ttk.Checkbutton(dataLF)
        self.chkRandomize_var = StringVar()
        self.chkRandomize.config(text="randomize", variable= self.chkRandomize_var, onvalue= "on" ,
                                 offvalue = "off", command= self.fRandomize)
        self.chkRandomize.grid(row=8,column=0, sticky='w')
        #
        self.eRandomize = ttk.Entry(dataLF, width=60)
        self.eRandomize.grid(row=8,column=1, sticky='we',padx=3)
        self.eRandomize.columnconfigure(0, weight=1)
        #--force-ssl         Force usage of SSL/HTTPS requests
        self.chkForceSsl = ttk.Checkbutton(dataLF)
        self.chkForceSsl_var = StringVar()
        self.chkForceSsl.config(text="force-ssl", variable= self.chkForceSsl_var, onvalue= "on" ,
                                offvalue = "off", command= self.fForceSsl)
        self.chkForceSsl.grid(row=9,column=0, sticky='w')
        #--host=HOST         HTTP Host header
        self.chkHOST = ttk.Checkbutton(dataLF)
        self.chkHOST_var = StringVar()
        self.chkHOST.config(text="host", variable= self.chkHOST_var, onvalue= "on" ,
                            offvalue = "off", command= self.fHost)
        self.chkHOST.grid(row=10,column=0, sticky='w')
        #
        self.eHOST = ttk.Entry(dataLF, width=60)
        self.eHOST.grid(row=10,column=1, sticky='we',padx=3)
        self.eHOST.columnconfigure(0, weight=1)
        #--referer=REFERER   HTTP Referer header
        self.chkReferer = ttk.Checkbutton(dataLF)
        self.chkReferer_var = StringVar()
        self.chkReferer.config(text="referer", variable= self.chkReferer_var, onvalue= "on" ,
                               offvalue = "off", command= self.fReferer)
        self.chkReferer.grid(row=11,column=0, sticky='w')
        #
        self.eReferer = ttk.Entry(dataLF, width=60)
        self.eReferer.grid(row=11,column=1, sticky='we',padx=3)
        self.eReferer.columnconfigure(0, weight=1)
        #    --headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123")
        self.chkHeaders = ttk.Checkbutton(dataLF)
        self.chkHeaders_var = StringVar()
        self.chkHeaders.config(text="headers", variable= self.chkHeaders_var, onvalue= "on" ,
                               offvalue = "off", command= self.fHeaders)
        self.chkHeaders.grid(row=12,column=0, sticky='w')
        #
        self.eHeaders = ttk.Entry(dataLF, width=60)
        self.eHeaders.grid(row=12,column=1, sticky='we',padx=3)
        self.eHeaders.columnconfigure(0, weight=1)
        #--proxy=PROXY       Use a HTTP proxy to connect to the target url
        self.chkPROXY = ttk.Checkbutton(dataLF)
        self.chkPROXY_var = StringVar()
        self.chkPROXY.config(text = "proxy", variable= self.chkPROXY_var, onvalue= "on" ,
                             offvalue = "off", command= self.fPROXY)
        self.chkPROXY.grid(row=13,column=0, sticky='w')
        #
        self.ePROXY = ttk.Entry(dataLF, width=60)
        self.ePROXY.grid(row =13,column=1, sticky='we',padx=3)
        self.ePROXY.columnconfigure(0, weight=1)
        #--proxy-cred=PCRED  HTTP proxy authentication credentials (name:password)
        self.chkPCRED = ttk.Checkbutton(dataLF)
        self.chkPCRED_var = StringVar()
        self.chkPCRED.config(text = "proxy-cred", variable= self.chkPCRED_var, onvalue= "on" ,
                             offvalue = "off", command= self.fPCRED)
        self.chkPCRED.grid(row=14,column=0, sticky='w')
        #
        self.ePCRED = ttk.Entry(dataLF, width=60)
        self.ePCRED.grid(row =14,column=1, sticky='we',padx=3)
        self.ePCRED.columnconfigure(0, weight=1)
        #--ignore-proxy      Ignore system default HTTP proxy
        self.chkPignore = ttk.Checkbutton(dataLF)
        self.chkPignore_var = StringVar()
        self.chkPignore.config(text = "ignore-proxy", variable= self.chkPignore_var, onvalue= "on" ,
                               offvalue = "off", command= self.fPignore)
        self.chkPignore.grid(row=15,column=0, sticky='w')
        #DATA2 #
        dataLF2 = ttk.Labelframe(data2, text='')
        dataLF2.grid(row = 0, column =0,pady=10,ipadx=3,ipady=3, sticky='we')
        #dataLF2.columnconfigure(0, weight=1)
        #--auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
        self.chkATYPE = ttk.Checkbutton(dataLF2)
        self.chkATYPE_var = StringVar()
        self.chkATYPE.config(text = "auth-type", variable= self.chkATYPE_var, onvalue= "on" ,
                             offvalue = "off", command= self.fATYPE)
        self.chkATYPE.grid(row=0,column=0, sticky='w')
        #
        self.eATYPE = ttk.Entry(dataLF2, width=60)
        self.eATYPE.grid(row =0,column=1, sticky='we',padx=3)
        self.eATYPE.columnconfigure(0, weight=1)
        #--auth-cred=ACRED   HTTP authentication credentials (name:password)
        self.chkACRED = ttk.Checkbutton(dataLF2)
        self.chkACRED_var = StringVar()
        self.chkACRED.config(text = "auth-cred", variable= self.chkACRED_var, onvalue= "on" ,
                             offvalue = "off", command= self.fACRED)
        self.chkACRED.grid(row=1,column=0, sticky='w')
        #
        self.eACRED = ttk.Entry(dataLF2, width=60)
        self.eACRED.grid(row =1,column=1, sticky='we',padx=3)
        self.eACRED.columnconfigure(0, weight=1)
        #--auth-cert=ACERT   HTTP authentication certificate (key_file,cert_file)
        self.chkACERT = ttk.Checkbutton(dataLF2)
        self.chkACERT_var = StringVar()
        self.chkACERT.config(text = "auth-cert", variable= self.chkACERT_var, onvalue= "on" ,
                             offvalue = "off", command= self.fACERT)
        self.chkACERT.grid(row=2,column=0, sticky='w')
        #
        #self.varACERT = StringVar()
        self.eACERT = ttk.Entry(dataLF2, width=60)
        #self.eACERT.config(text="", textvariable = self.varACERT)
        self.eACERT.grid(row =2,column=1, sticky='we',padx=3)
        self.eACERT.columnconfigure(0, weight=1)
        #--delay=DELAY       Delay in seconds between each HTTP request
        self.chkDELAY = ttk.Checkbutton(dataLF2)
        self.chkDELAY_var = StringVar()
        self.chkDELAY.config(text = "delay", variable= self.chkDELAY_var, onvalue= "on" ,
                             offvalue = "off", command= self.fDELAY)
        self.chkDELAY.grid(row=6,column=0, sticky='w')
        #
        self.eDELAY = ttk.Entry(dataLF2, width=60)
        self.eDELAY.grid(row =6,column=1, sticky='we',padx=3)
        self.eDELAY.columnconfigure(0, weight=1)
        #--timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
        self.chkTIMEOUT = ttk.Checkbutton(dataLF2)
        self.chkTIMEOUT_var = StringVar()
        self.chkTIMEOUT.config(text = "timeout", variable= self.chkTIMEOUT_var, onvalue= "on" ,
                               offvalue = "off", command= self.fTIMEOUT)
        self.chkTIMEOUT.grid(row=7,column=0, sticky='w')
        #
        self.eTIMEOUT = ttk.Entry(dataLF2, width=60)
        self.eTIMEOUT.grid(row =7,column=1, sticky='we',padx=3)
        self.eTIMEOUT.columnconfigure(0, weight=1)
        #--retries=RETRIES   Retries when the connection timeouts (default 3)
        self.chkRETRIES = ttk.Checkbutton(dataLF2)
        self.chkRETRIES_var = StringVar()
        self.chkRETRIES.config(text = "retries", variable= self.chkRETRIES_var, onvalue= "on" ,
                               offvalue = "off", command= self.fRETRIES)
        self.chkRETRIES.grid(row=8,column=0, sticky='w')
        #
        self.eRETRIES = ttk.Entry(dataLF2, width=60)
        self.eRETRIES.grid(row =8,column=1, sticky='we',padx=3)
        self.eRETRIES.columnconfigure(0, weight=1)
        #--scope=SCOPE       Regexp to filter targets from provided proxy log
        self.chkSCOPE = ttk.Checkbutton(dataLF2)
        self.chkSCOPE_var = StringVar()
        self.chkSCOPE.config(text = "scope", variable= self.chkSCOPE_var, onvalue= "on" ,
                             offvalue = "off", command= self.fSCOPE)
        self.chkSCOPE.grid(row=9,column=0, sticky='w')
        #
        self.eSCOPE = ttk.Entry(dataLF2, width=60)
        self.eSCOPE.grid(row =9,column=1, sticky='we',padx=3)
        self.eSCOPE.columnconfigure(0, weight=1)
        #--safe-url=SAFURL   Url address to visit frequently during testing
        self.chkSAFURL = ttk.Checkbutton(dataLF2)
        self.chkSAFURL_var = StringVar()
        self.chkSAFURL.config(text = "safe-url", variable= self.chkSAFURL_var, onvalue= "on" ,
                              offvalue = "off", command= self.fSAFURL)
        self.chkSAFURL.grid(row=10,column=0, sticky='w')
        #
        self.eSAFURL = ttk.Entry(dataLF2, width=60)
        self.eSAFURL.grid(row =10,column=1, sticky='we',padx=3)
        self.eSAFURL.columnconfigure(0, weight=1)
        #--safe-freq=SAFREQ  Test requests between two visits to a given safe url
        self.chkSAFREQ = ttk.Checkbutton(dataLF2)
        self.chkSAFREQ_var = StringVar()
        self.chkSAFREQ.config(text = "safe-freq", variable= self.chkSAFREQ_var, onvalue= "on" ,
                              offvalue = "off", command= self.fSAFREQ)
        self.chkSAFREQ.grid(row=11,column=0, sticky='w')
        #
        self.eSAFREQ = ttk.Entry(dataLF2, width=60)
        self.eSAFREQ.grid(row =11,column=1, sticky='we',padx=3)
        self.eSAFREQ.columnconfigure(0, weight=1)
        #--skip-urlencode    Skip URL encoding of POST data
        self.chkSkipUrlencode = ttk.Checkbutton(dataLF2)
        self.chkSkipUrlencode_var = StringVar()
        self.chkSkipUrlencode.config(text = "skip-urlencode", variable= self.chkSkipUrlencode_var, onvalue= "on" ,
                                     offvalue = "off", command= self.fSkipUrlencode)
        self.chkSkipUrlencode.grid(row=12,column=0, sticky='w')
        #--eval=EVALCODE     Evaluate provided Python code before the request (e.g.
                    #"import hashlib;id2=hashlib.md5(id).hexdigest()")
        self.chkEVALCODE = ttk.Checkbutton(dataLF2)
        self.chkEVALCODE_var = StringVar()
        self.chkEVALCODE.config(text = "eval", variable= self.chkEVALCODE_var, onvalue= "on" ,
                                offvalue = "off", command= self.fEVALCODE)
        self.chkEVALCODE.grid(row=13,column=0, sticky='w')
        #
        self.eEVALCODE = ttk.Entry(dataLF2, width=60)
        self.eEVALCODE.grid(row =13,column=1, sticky='we',padx=3)
        self.eEVALCODE.columnconfigure(0, weight=1)
        #
        enumerateLF = ttk.Labelframe(enumerationF, text='')
        enumerateLF.grid(row = 0, column = 0, ipadx=3,padx=3, pady = 3, sticky='nw')
        # Retrieve DBMS current user
        self.chkCurrent_user = ttk.Checkbutton(enumerateLF)
        self.chkCurrent_user_var = StringVar()
        self.chkCurrent_user.config(text="current-user", variable= self.chkCurrent_user_var, onvalue= "on" ,
                                    offvalue = "off", command= self.chekCurrent_user)
        self.chkCurrent_user.grid(row=0,column=0,sticky = 'w')
        # Retrieve DBMS current database
        self.chkCurrent_db = ttk.Checkbutton(enumerateLF)
        self.chkCurrent_db_var = StringVar()
        self.chkCurrent_db.config(text="current-db", variable= self.chkCurrent_db_var, onvalue= "on" ,
                                  offvalue = "off", command= self.chekCurrent_db)
        self.chkCurrent_db.grid(row=1,column=0,sticky = 'w')
        #--is-dba   Detect if the DBMS current user is DBA
        self.chk_is_dba = ttk.Checkbutton(enumerateLF)
        self.chk_is_dba_var = StringVar()
        self.chk_is_dba.config(text="is-dba", variable= self.chk_is_dba_var, onvalue= "on" ,
                               offvalue = "off", command= self.chek_is_dba)
        self.chk_is_dba.grid(row=2,column=0,sticky = 'w')
        #--users             Enumerate DBMS users
        self.chk_users = ttk.Checkbutton(enumerateLF)
        self.chk_users_var = StringVar()
        self.chk_users.config(text="users", variable= self.chk_users_var, onvalue= "on" ,
                              offvalue = "off", command= self.chek_users)
        self.chk_users.grid(row=3,column=0,sticky = 'w')
        #-passwords         Enumerate DBMS users password hashes
        self.chk_passwords = ttk.Checkbutton(enumerateLF)
        self.chk_passwords_var = StringVar()
        self.chk_passwords.config(text="passwords", variable= self.chk_passwords_var, onvalue= "on" ,
                                  offvalue = "off", command= self.chek_passwords)
        self.chk_passwords.grid(row=0,column=1,sticky = 'w')
        #--privileges        Enumerate DBMS users privileges
        self.chk_privileges  = ttk.Checkbutton(enumerateLF)
        self.chk_privileges_var = StringVar()
        self.chk_privileges.config(text="privileges", variable= self.chk_privileges_var, onvalue= "on" ,
                                   offvalue = "off", command= self.chek_privileges)
        self.chk_privileges.grid(row=1,column=1,sticky = 'w')
        #--roles             Enumerate DBMS users roles
        self.chk_roles = ttk.Checkbutton(enumerateLF)
        self.chk_roles_var = StringVar()
        self.chk_roles .config(text="roles", variable= self.chk_roles_var, onvalue= "on" ,
                               offvalue = "off", command= self.chek_roles)
        self.chk_roles.grid(row=2,column=1,sticky = 'w')
        #-dbs               Enumerate DBMS databases
        self.chk_dbs = ttk.Checkbutton(enumerateLF)
        self.chk_dbs_var = StringVar()
        self.chk_dbs.config(text="dbs", variable= self.chk_dbs_var, onvalue= "on" ,
                            offvalue = "off", command= self.chek_dbs)
        self.chk_dbs.grid(row=3,column=1,sticky = 'w')
        #--tables            Enumerate DBMS database tables
        self.chk_tables = ttk.Checkbutton(enumerateLF)
        self.chk_tables_var = StringVar()
        self.chk_tables.config(text="tables", variable= self.chk_tables_var, onvalue= "on" ,
                               offvalue = "off", command= self.chek_tables)
        self.chk_tables.grid(row=0,column=2,sticky = 'w')
        #--columns           Enumerate DBMS database table columns
        self.chk_columns = ttk.Checkbutton(enumerateLF)
        self.chk_columns_var = StringVar()
        self.chk_columns.config(text="columns", variable= self.chk_columns_var, onvalue= "on" ,
                                offvalue = "off", command= self.chek_columns)
        self.chk_columns.grid(row=1,column=2,sticky = 'w')
        #--schema            Enumerate DBMS schema
        self.chk_schema = ttk.Checkbutton(enumerateLF)
        self.chk_schema_var = StringVar()
        self.chk_schema.config(text="schema", variable= self.chk_schema_var, onvalue= "on" ,
                               offvalue = "off", command= self.chek_schema)
        self.chk_schema.grid(row=2,column=2,sticky = 'w')
        #--count             Retrieve number of entries for table(s)
        self.chk_count  = ttk.Checkbutton(enumerateLF)
        self.chk_count_var = StringVar()
        self.chk_count.config(text="count", variable= self.chk_count_var, onvalue= "on" ,
                              offvalue = "off", command= self.chek_count)
        self.chk_count.grid(row=3,column=2,sticky = 'w')
        #--dump              Dump DBMS database table entries
        dumpLF = ttk.Labelframe(enumerationF, text='')
        dumpLF.grid(row = 0, column=1, ipadx=3,pady = 3, padx=3, sticky='nw')
        #
        # Banner
        self.chk_Banner = ttk.Checkbutton(dumpLF)
        self.chk_Banner_var = StringVar()
        self.chk_Banner.config(text="banner", variable= self.chk_Banner_var, onvalue= "on",
                               offvalue = "off", command= self.chekBanner)
        self.chk_Banner.grid(row=0,column=0, sticky= 'w')
        #
        self.chk_dump = ttk.Checkbutton(dumpLF)
        self.chk_dump_var = StringVar()
        self.chk_dump.config(text="dump", variable= self.chk_dump_var, onvalue= "on" ,
                             offvalue = "off", command= self.chek_dump)
        self.chk_dump.grid(row=1,column=0,sticky = 'w')
        #--dump-all          Dump all DBMS databases tables entries
        self.chk_dump_all = ttk.Checkbutton(dumpLF)
        self.chk_dump_all_var = StringVar()
        self.chk_dump_all.config(text="dump-all", variable= self.chk_dump_all_var, onvalue= "on" ,
                                 offvalue = "off", command= self.chek_dump_all)
        self.chk_dump_all.grid(row=2,column=0,sticky = 'w')
        #--search            Search column(s), table(s) and/or database name(s)
        self.chk_search = ttk.Checkbutton(dumpLF)
        self.chk_search_var = StringVar()
        self.chk_search.config(text="search", variable= self.chk_search_var, onvalue= "on" ,
                               offvalue = "off", command= self.chek_search)
        self.chk_search.grid(row=3,column=0,sticky = 'w')
        #--exclude-sysdbs    Exclude DBMS system databases when enumerating tables
        self.chk_exclude = ttk.Checkbutton(dumpLF)
        self.chk_exclude_var = StringVar()
        self.chk_exclude.config(text="exclude-sysdbs", variable= self.chk_exclude_var, onvalue= "on" ,
                                offvalue = "off", command= self.chek_exclude)
        self.chk_exclude.grid(row=0,column=1,sticky = 'w',padx=3)
        #--first=FIRSTCHAR   First query output word character to retrieve
        self.chk_first = ttk.Checkbutton(dumpLF)
        self.chk_first_var = StringVar()
        self.chk_first.config(text="first CHAR", variable= self.chk_first_var, onvalue= "on" ,
                              offvalue = "off", command= self.chek_first)
        self.chk_first.grid(row=1,column = 1,sticky='w',padx=3)
        #
        self.entry_first= ttk.Entry(dumpLF)
        self.entry_first.config(text="" , textvariable="", width = 3)
        self.entry_first.grid(row=1,column=2,sticky='w')
        #--last=LASTCHAR     Last query output word character to retrieve
        self.chk_last = ttk.Checkbutton(dumpLF)
        self.chk_last_var = StringVar()
        self.chk_last.config(text="last CHAR", variable= self.chk_last_var, onvalue= "on" ,
                             offvalue = "off", command= self.chek_last)
        self.chk_last.grid(row=2,column = 1,sticky='w',padx=3)
        #
        self.entry_last= ttk.Entry(dumpLF)
        self.entry_last.config(text="" , textvariable="", width = 3)
        self.entry_last.grid(row=2,column=2,sticky='w')
        #-D DB               DBMS database to enumerate
        dtcLF = ttk.Labelframe(enumerationF, text='')
        dtcLF.grid(row = 1, column=0, pady = 10, padx=5, sticky='we', columnspan=5)
        dtcLF.columnconfigure(0, weight=1)
        #
        self.entryD = ttk.Entry(dtcLF,width=68)
        self.entryD.config(text="" , textvariable="")
        self.entryD.grid(row=0,column=1, sticky='e',padx=3)
        #
        self.chkD = ttk.Checkbutton(dtcLF)
        self.chkD_var = StringVar()
        self.chkD.config(text="DB", variable= self.chkD_var, onvalue= "on" ,
                         offvalue = "off", command= self.chekD)
        self.chkD.grid(row=0,column = 0, sticky = 'w')
        #-T TBL              DBMS database table to enumerate
        self.entryT = ttk.Entry(dtcLF,width=68)
        self.entryT.config(text="" , textvariable="")
        self.entryT.grid(row=1,column=1, sticky='w',padx=3)
        self.chkT = ttk.Checkbutton(dtcLF)
        self.chkT_var = StringVar()
        self.chkT.config(text="TBL", variable= self.chkT_var, onvalue= "on" ,
                         offvalue = "off", command= self.chekT)
        self.chkT.grid(row=1,column = 0, sticky = 'w')
        #-C COL              DBMS database table column to enumerate
        self.entryC = ttk.Entry(dtcLF,width=68)
        self.entryC.config(text="" , textvariable="")
        self.entryC.grid(row=2,column=1, sticky='w',padx=3)
        #
        self.chkC = ttk.Checkbutton(dtcLF)
        self.chkC_var = StringVar()
        self.chkC.config(text="COL", variable= self.chkC_var, onvalue= "on" ,
                         offvalue = "off", command= self.chekC)
        self.chkC.grid(row=2,column = 0, sticky = 'w')
        #-U USER
        self.chkUSER = ttk.Checkbutton(dtcLF)
        self.chkUSER_var = StringVar()
        self.chkUSER.config(text="USER", variable= self.chkUSER_var, onvalue= "on" ,
                            offvalue = "off", command= self.fUSER)
        self.chkUSER.grid(row=3,column=0, sticky='w')
        #
        self.eUSER = ttk.Entry(dtcLF,width=68)
        self.eUSER.config(text="" , textvariable="")
        self.eUSER.grid(row=3,column=1, sticky='w',padx=3)
        #LIMIT
        self.chk_start = ttk.Checkbutton(dtcLF)
        self.chk_start_var = StringVar()
        self.chk_start.config(text="Limit", variable= self.chk_start_var, onvalue= "on" ,
                              offvalue = "off", command= self.chek_start_stop)
        self.chk_start.grid(row=4,column = 0, sticky = 'w')
        #
        self.varE_start = StringVar()
        self.varE_start.set("star,stop")
        self.entry_start= ttk.Entry(dtcLF,width=68)
        self.entry_start.config(text="" , textvariable= self.varE_start)
        self.entry_start.grid(row=4,column=1, sticky='w',padx=3)
        #
        sqlQueryLF = ttk.Labelframe(enumerationF, text='')
        sqlQueryLF.grid(row = 2, column=0, pady = 10, padx=5, sticky='we', columnspan=5)
        sqlQueryLF.columnconfigure(0, weight=1)
        # --sql-query=
        self.chkQuery = ttk.Checkbutton(sqlQueryLF)
        self.chkQuery_var = StringVar()
        self.chkQuery.config(text="sql-query", variable= self.chkQuery_var, onvalue= "on" ,
                             offvalue = "off", command= self.chekQuery)
        self.chkQuery.grid(row=0,column=0,sticky = 'w')
        #
        self.entryQuery = ttk.Entry(sqlQueryLF,width=68)
        self.entryQuery.config(text="" , textvariable="")
        self.entryQuery.grid(row=0,column=1, sticky='w',padx=3)
        #--sql-shell
        self.chkSqlShell  = ttk.Checkbutton(sqlQueryLF)
        self.chkSqlShell_var = StringVar()
        self.chkSqlShell.config(text="sql-shell", variable= self.chkSqlShell_var, onvalue= "on" ,
                              offvalue = "off", command= self.fSqlShell)
        self.chkSqlShell.grid(row=1,column=0,sticky = 'w')

        #Brute force
        charbfLF = ttk.Labelframe(enumerationF, text='Brute force')
        charbfLF.grid(row = 0, column = 3,padx=3,pady=3, sticky='nw')
        #--common-tables     Check existence of common tables
        self.chkBFt = ttk.Checkbutton(charbfLF)
        self.chkBFt_var = StringVar()
        self.chkBFt.config(text="common-tables", variable= self.chkBFt_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekBFt)
        self.chkBFt.grid(row=0,column = 0,sticky = 'w')
        #--common-columns    Check existence of common columns
        self.chkBFc = ttk.Checkbutton(charbfLF)
        self.chkBFc_var = StringVar()
        self.chkBFc.config(text="common-columns", variable= self.chkBFc_var, onvalue= "on" ,
                           offvalue = "off", command= self.chekBFc)
        self.chkBFc.grid(row=1,column = 0,sticky = 'w')
        # Access
        AccessF = ttk.Notebook(fileF)
        fileAcc = ttk.Frame(AccessF)
        OsAcc = ttk.Frame(AccessF)
        WinRegAcc = ttk.Frame(AccessF)
        AccessF.add(fileAcc, text='File system')
        AccessF.add(OsAcc, text='Operating system')
        AccessF.add(WinRegAcc, text='Windows registry')
        AccessF.columnconfigure(0, weight=1)
        AccessF.grid(sticky = 'nswe',pady=5,padx=5)
        #
        fileAcc.columnconfigure(0, weight=1)
        #OsAcc.columnconfigure(0, weight=1)
        #WinRegAcc.columnconfigure(0, weight=1)
        # File system access:
        filereadLF = ttk.Labelframe(fileAcc, text='')
        filereadLF.grid(sticky='we', ipady=3)
        #filereadLF.columnconfigure(0, weight=1)
        #--file-read=RFILE   Read a file from the back-end DBMS file system:
        self.chkFile = ttk.Checkbutton(filereadLF)
        self.chkFile_var = StringVar()
        self.chkFile.config(text="file-read ", variable= self.chkFile_var, onvalue= "on" ,
                            offvalue = "off", command= self.chekFile)
        self.chkFile.grid(row=0,column=0,sticky = 'w')
        #
        self.entryFile = ttk.Entry(filereadLF,width=62)
        self.entryFile.grid(row=0,column=1, sticky='w',padx=3)
        #--file-write=WFILE  Write a local file on the back-end DBMS file system
        self.varWFILE = StringVar()
        self.chkWFILE = ttk.Checkbutton(filereadLF)
        self.chkWFILE.config(text="file-write", variable= self.varWFILE, onvalue= "on" ,
                             offvalue = "off", command= self.fWFILE)
        self.chkWFILE.grid(row=1,column=0,sticky = 'w')
        #
        self.eWFILE_var = StringVar()
        self.eWFILE = ttk.Entry(filereadLF,width=62)
        self.eWFILE.config(text="", textvariable=self.eWFILE_var)
        self.eWFILE.grid(row=1,column=1, sticky='w',padx=3)
        #
        self.file_WFILE = options_WFILE = {}
        options_WFILE['defaultextension'] = ''
        options_WFILE['filetypes'] = [('all files', '.*')]
        options_WFILE['initialdir'] = './SQM/SHELL/'
        options_WFILE['parent'] = WatchLog
        options_WFILE['title'] = 'Open WFILE'
        #--file-dest=DFILE   Back-end DBMS absolute filepath to write to:
        self.chkDFILE = ttk.Checkbutton(filereadLF)
        self.chkDFILE_var = StringVar()
        self.chkDFILE.config(text="file-dest ", variable= self.chkDFILE_var, onvalue= "on" ,
                             offvalue = "off")#, command= self.fDFILE)
        self.chkDFILE.grid(row=2,column=0,sticky = 'w')
        #
        self.eDFILE = ttk.Entry(filereadLF,width=62)
        self.eDFILE.grid(row=2,column=1, sticky='w',padx=3)
        # BUTTON
        self.viewfile = ttk.Button(filereadLF,width=7)
        self.viewfile.config(text ="view log", command=self.vfile)
        self.viewfile.grid(row =0, column=3,sticky='ne',rowspan=2)
        #Default *log,*config
        configDL = ttk.Panedwindow(fileAcc, orient=HORIZONTAL, width=100, height=240)
        configDL.rowconfigure( 0, weight=1 )
        configDL.columnconfigure( 0, weight=1)
        #
        catLF = ttk.Labelframe(configDL, text='Category')
        catLF.rowconfigure( 0, weight=1 )
        catLF.columnconfigure( 0, weight=1 )
        #
        listLF = ttk.Labelframe(configDL, text='Default *log, *config')
        listLF.rowconfigure( 0, weight=1 )
        listLF.columnconfigure( 0, weight=1 )
        #
        configDL.add(catLF)
        configDL.add(listLF)
        configDL.grid(row=1,columnspan=2, sticky='we', pady=5)
        #Category ./SQM/PATH_TRAVERSAL*.txt
        self.Lcat = Listbox(catLF,height=100,width=20,selectmode=EXTENDED)

        files_cat = os.listdir('./SQM/PATH_TRAVERSAL')
        cats = filter(lambda x: x.endswith('.txt'), files_cat)
        for cat_list in cats:
            cat_list = cat_list.replace('.txt', '')
            self.Lcat.insert(END, cat_list)
        self.Lcat.grid(row =0, column = 0,sticky='we')
        self.Lcat.columnconfigure( 0, weight=1 )
        self.Lcat.bind("<Double-Button-1>", self.show_def_log)
        # Scroll
        scrollcat = ttk.Scrollbar(catLF, orient=VERTICAL, command=self.Lcat.yview)
        self.Lcat['yscrollcommand'] = scrollcat.set
        scrollcat.grid(row=0,column=1, sticky='ns')
        #Show Default *log, *config
        s_def_log = ttk.Scrollbar(listLF)
        s_def_log.grid(row=0, column=1, sticky='ns')
        #
        self.d_log_TXT = Text(listLF, yscrollcommand=s_def_log.set, width = 73,
                              height=50,bg='#002B36', fg='#93A1A1')
        s_def_log.config(command= self.d_log_TXT.yview)
        self.d_log_TXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
        #Operating system access:
        OsAccLF = ttk.Labelframe(OsAcc, text='')
        OsAccLF.grid(sticky='we', ipady=3)
        OsAccLF.columnconfigure(0, weight=1)
        #--os-cmd=OSCMD      Execute an operating system command
        self.chkOSCMD = ttk.Checkbutton(OsAccLF)
        self.chkOSCMD_var = StringVar()
        self.chkOSCMD.config(text="os-cmd", variable= self.chkOSCMD_var, onvalue= "on" ,
                             offvalue = "off", command= self.fOSCMD)
        self.chkOSCMD.grid(row=0,column=0,sticky = 'w')
        #
        self.eOSCMD = ttk.Entry(OsAccLF,width=68)
        self.eOSCMD.grid(row=0,column=1, sticky='we',padx=3)
        #--os-shell          Prompt for an interactive operating system shell
        self.chkShell = ttk.Checkbutton(OsAccLF)
        self.chkShell_var = StringVar()
        self.chkShell.config(text="os-shell", variable= self.chkShell_var, onvalue= "on" ,
                             offvalue = "off", command= self.fShell)
        self.chkShell.grid(row=1,column=0,sticky = 'w')
        #--os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
        self.chkPWN = ttk.Checkbutton(OsAccLF)
        self.chkPWN_var = StringVar()
        self.chkPWN.config(text="os-pwn", variable= self.chkPWN_var, onvalue= "on" ,
                           offvalue = "off", command= self.fPWN)
        self.chkPWN.grid(row=2,column=0,sticky = 'w')
        #--os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
        self.chkSmbrelay = ttk.Checkbutton(OsAccLF)
        self.chkSmbrelay_var = StringVar()
        self.chkSmbrelay.config(text="os-smbrelay", variable= self.chkSmbrelay_var, onvalue= "on" ,
                                offvalue = "off", command= self.fSmbrelay)
        self.chkSmbrelay.grid(row=3,column=0,sticky = 'w')
        #--os-bof            Stored procedure buffer overflow exploitation
        self.chkBOF = ttk.Checkbutton(OsAccLF)
        self.chkBOF_var = StringVar()
        self.chkBOF.config(text="os-bof", variable= self.chkBOF_var, onvalue= "on" ,
                           offvalue = "off", command= self.fBOF)
        self.chkBOF.grid(row=4,column=0,sticky = 'w')
        #--priv-esc          Database process' user privilege escalation
        self.chkPrivEsc = ttk.Checkbutton(OsAccLF)
        self.chkPrivEsc_var = StringVar()
        self.chkPrivEsc.config(text="priv-esc", variable= self.chkPrivEsc_var, onvalue= "on" ,
                               offvalue = "off", command= self.fPrivEsc)
        self.chkPrivEsc.grid(row=5,column=0,sticky = 'w')
        #--msf-path=MSFPATH  Local path where Metasploit Framework is installed
        self.chkMSFPATH = ttk.Checkbutton(OsAccLF)
        self.chkMSFPATH_var = StringVar()
        self.chkMSFPATH.config(text="msf-path", variable= self.chkMSFPATH_var, onvalue= "on" ,
                               offvalue = "off", command= self.fMSFPATH)
        self.chkMSFPATH.grid(row=6,column=0,sticky = 'w')
        #
        self.eMSFPATH_var = StringVar()
        self.eMSFPATH = ttk.Entry(OsAccLF,width=68)
        self.eMSFPATH.grid(row=6,column=1, sticky='we',padx=3)
        self.eMSFPATH.config(text="",textvariable=self.eMSFPATH_var)
        #--tmp-path=TMPPATH  Remote absolute path of temporary files directory
        self.chkTMPPATH = ttk.Checkbutton(OsAccLF)
        self.chkTMPPATH_var = StringVar()
        self.chkTMPPATH.config(text="tmp-path", variable= self.chkTMPPATH_var, onvalue= "on" ,
                             offvalue = "off", command= self.fTMPPATH)
        self.chkTMPPATH.grid(row=7,column=0,sticky = 'w')
        #
        self.eTMPPATH = ttk.Entry(OsAccLF,width=68)
        self.eTMPPATH.grid(row=7,column=1, sticky='we',padx=3)
        #Windows registry access:
        WinRegAccLF = ttk.Labelframe(WinRegAcc, text='')
        WinRegAccLF.grid(sticky='we', ipady=3)
        WinRegAccLF.columnconfigure(0, weight=1)
        #--reg-read          Read a Windows registry key value
        self.chkRegRead = ttk.Checkbutton(WinRegAccLF)
        self.chkRegRead_var = StringVar()
        self.chkRegRead.config(text="reg-read", variable= self.chkRegRead_var, onvalue= "on" ,
                             offvalue = "off", command= self.fRegRead)
        self.chkRegRead.grid(row=0,column=0,sticky = 'w')
        #--reg-add           Write a Windows registry key value data
        self.chkRegAdd = ttk.Checkbutton(WinRegAccLF)
        self.chkRegAdd_var = StringVar()
        self.chkRegAdd.config(text="reg-add", variable= self.chkRegAdd_var, onvalue= "on" ,
                               offvalue = "off", command= self.fRegAdd)
        self.chkRegAdd.grid(row=1,column=0,sticky = 'w')
        #--reg-del           Delete a Windows registry key value
        self.chkRegDel = ttk.Checkbutton(WinRegAccLF)
        self.chkRegDel_var = StringVar()
        self.chkRegDel.config(text="reg-del", variable= self.chkRegDel_var, onvalue= "on" ,
                               offvalue = "off", command= self.fRegDel)
        self.chkRegDel.grid(row=2,column=0,sticky = 'w')
        #--reg-key=REGKEY    Windows registry key
        self.chkREGKEY = ttk.Checkbutton(WinRegAccLF)
        self.chkREGKEY_var = StringVar()
        self.chkREGKEY.config(text="reg-key", variable= self.chkREGKEY_var, onvalue= "on" ,
                               offvalue = "off", command= self.fREGKEY)
        self.chkREGKEY.grid(row=3,column=0,sticky = 'w')
        #
        self.eREGKEY = ttk.Entry(WinRegAccLF,width=68)
        self.eREGKEY.grid(row=3,column=1, sticky='we',padx=3)
        #--reg-value=REGVAL  Windows registry key value
        self.chkREGVAL = ttk.Checkbutton(WinRegAccLF)
        self.chkREGVAL_var = StringVar()
        self.chkREGVAL.config(text="reg-value", variable= self.chkREGVAL_var, onvalue= "on" ,
                               offvalue = "off", command= self.fREGVAL)
        self.chkREGVAL.grid(row=4,column=0,sticky = 'w')
        #
        self.eREGVAL = ttk.Entry(WinRegAccLF,width=68)
        self.eREGVAL.grid(row=4,column=1, sticky='we',padx=3)
        #--reg-data=REGDATA  Windows registry key value data
        self.chkREGDATA = ttk.Checkbutton(WinRegAccLF)
        self.chkREGDATA_var = StringVar()
        self.chkREGDATA.config(text="reg-data", variable= self.chkREGDATA_var, onvalue= "on" ,
                               offvalue = "off", command= self.fREGDATA)
        self.chkREGDATA.grid(row=5,column=0,sticky = 'w')
        #
        self.eREGDATA = ttk.Entry(WinRegAccLF,width=68)
        self.eREGDATA.grid(row=5,column=1, sticky='we',padx=3)
        #--reg-type=REGTYPE  Windows registry key value type
        self.chkREGTYPE = ttk.Checkbutton(WinRegAccLF)
        self.chkREGTYPE_var = StringVar()
        self.chkREGTYPE.config(text="reg-type", variable= self.chkREGTYPE_var, onvalue= "on" ,
                               offvalue = "off", command= self.fREGTYPE)
        self.chkREGTYPE.grid(row=6,column=0,sticky = 'w')
        #
        self.eREGTYPE = ttk.Entry(WinRegAccLF,width=68)
        self.eREGTYPE.grid(row=6,column=1, sticky='we',padx=3)
    # ####################################################
    #                Functions:                          #
    # ####################################################
    #Targets:
    def fTarget(self):
        try:
            selection = self.varTarget.get()
            if selection == "url":
                pass
            elif selection == "logFile":
                filename = tkFileDialog.askopenfile(mode='r')
                self.urlentry.set(filename.name)
            elif selection == "bulkFile":
                filename = tkFileDialog.askopenfile(mode='r')
                self.urlentry.set(filename.name)
            elif selection == "requestFile":
                filename = tkFileDialog.askopenfile(mode='r', **self.file_request_save)
                self.urlentry.set(filename.name)
            elif selection == "googleDork":
                pass
            elif selection == "direct":
                pass
            elif selection == "configFile":
                filename = tkFileDialog.askopenfile(mode='r', **self.file_ini)
                self.urlentry.set(filename.name)
        except:
            pass
    #--beep              Sound alert when SQL injection found
    def fBeep(self):
        sqlBeep = self.chkBeep_var.get()
        if sqlBeep == "on" :
            Beep_sql= ' --beep'
        else:
            Beep_sql= ""
        return Beep_sql
    #--check-payload     Offline WAF/IPS/IDS payload detection testing
    def fPayload(self):
        sqlPayload = self.chkPayload_var.get()
        if sqlPayload == "on" :
            Payload_sql= ' --check-payload'
        else:
            Payload_sql= ""
        return Payload_sql
    #--check-waf         Check for existence of WAF/IPS/IDS protection
    def fWaf(self):
        sqlWaf = self.chkWaf_var.get()
        if sqlWaf == "on" :
            Waf_sql= ' --check-waf'
        else:
            Waf_sql= ""
        return Waf_sql
    #--cleanup           Clean up the DBMS by sqlmap specific UDF and tables
    def fCleanup(self):
        sqlCleanup = self.chkCleanup_var.get()
        if sqlCleanup == "on" :
            Cleanup_sql= ' --cleanup'
        else:
            Cleanup_sql= ""
        return Cleanup_sql
    #--dependencies      Check for missing sqlmap dependencies
    def fDependencies(self):
        sqlDependencies = self.chkDependencies_var.get()
        if sqlDependencies == "on" :
            Dependencies_sql= ' --dependencies'
        else:
            Dependencies_sql= ""
        return Dependencies_sql
    #--gpage=GOOGLEPAGE  Use Google dork results from specified page number
    def fGpage(self):
        sqlGpage = self.chkGpage_var.get()
        if sqlGpage == "on" :
            Gpage_sql= ' --gpage=%s' % (self.eGpage.get())
        else:
            Gpage_sql= ""
        return Gpage_sql
    #--disable-hash
    def fDHash(self):
        sqlDHash = self.chkDHash_var.get()
        if sqlDHash == "on" :
            DHash_sql= ' --disable-hash'
        else:
            DHash_sql= ""
        return DHash_sql
    #--disable-like
    def fDLike(self):
        sqlDLike = self.chkDLike_var.get()
        if sqlDLike == "on" :
            DLike_sql= ' --disable-like'
        else:
            DLike_sql= ""
        return DLike_sql
    #fTSTF
    def fTSTF(self):
        sqlTSTF = self.chkTSTF_var.get()
        if sqlTSTF == "on" :
            TSTF_sql= ' --test-filter=%s' % (self.eTSTF.get())
        else:
            TSTF_sql= ""
        return TSTF_sql
    #--Exact
    def fExact(self):
        sqlExact = self.chkExact_var.get()
        if sqlExact == "on" :
            Exact_sql= ' --exact'
        else:
            Exact_sql= ""
        return Exact_sql
    #--mobile            Imitate smartphone through HTTP User-Agent header
    def fMobile(self):
        sqlMobile = self.chkMobile_var.get()
        if sqlMobile == "on" :
            Mobile_sql= ' --mobile'
        else:
            Mobile_sql= ""
        return Mobile_sql
    #--page-rank         Display page rank (PR) for Google dork results
    def fRank(self):
        sqlRank = self.chkRank_var.get()
        if sqlRank == "on" :
            Rank_sql= ' --page-rank'
        else:
            Rank_sql= ""
        return Rank_sql
    #--purge-output      Safely remove all content from output directory
    def fPurge(self):
        sqlPurge = self.chkPurge_var.get()
        if sqlPurge == "on" :
            Purge_sql= ' --purge-output'
        else:
            Purge_sql= ""
        return Purge_sql
    #--smart             Conduct through tests only if positive heuristic(s)
    def fSmart(self):
        sqlSmart = self.chkSmart_var.get()
        if sqlSmart == "on" :
            Smart_sql= ' --smart'
        else:
            Smart_sql= ""
        return Smart_sql
    #--wizard            Simple wizard interface for beginner users

    #-s SESSIONFILE      Save and resume all data retrieved on a session file
    def fSesFile(self,*args):
        sql_SesFile = self.chkSesFile_var.get()
        if sql_SesFile == "on" :
            SesFile_sql= ' -s ./SQM/SESSION/%s' % (self.eSesFile.get())
        else:
            SesFile_sql= ""
        return SesFile_sql
    #-t TRAFFICFILE      Log all HTTP traffic into a textual file
    def fTrafFile(self,*args):
        sql_TrafFile = self.chkTrafFile_var.get()
        if sql_TrafFile == "on" :
            TrafFile_sql= ' -t ./SQM/TRAFFIC/%s' % (self.eTrafFile.get())
        else:
            TrafFile_sql= ""
        return TrafFile_sql

    #Open Session FILE
    def fSes(self):
        sesfile = tkFileDialog.askopenfile(mode='r', **self.file_session)
        if sesfile:
            self.sesTXT.delete("1.0",END)
            ses = sesfile.read()
            self.sesTXT.insert(END, ses)
            self.sesTXT.mark_set(INSERT, '1.0')
            self.sesTXT.focus()
    # Open Traffic FILE
    def fTraf(self):
        traffile = tkFileDialog.askopenfile(mode='r', **self.file_traf)
        if traffile:
            self.sesTXT.delete("1.0",END)
            traf = traffile.read()
            self.sesTXT.insert(END, traf)
            self.sesTXT.mark_set(INSERT, '1.0')
            self.sesTXT.focus()
    #Req.File/Load/Save
    def saveReqF(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_request_save)
        if filename:
            textoutput = self.reqFile.get(0.0, END)
            open(filename, 'w').write(textoutput)

    def openReqF(self):
        filename = tkFileDialog.askopenfile(mode='r', **self.file_request_save)
        if filename:
            self.reqFile.delete("1.0",END)
            req = filename.read()
            self.reqFile.insert(END, req)
            self.reqFile.mark_set(INSERT, '1.0')
            self.reqFile.focus()
    #
    def openIniF(self):
        #self.file_ini
        filename = tkFileDialog.askopenfile(mode='r', **self.file_ini)
        if filename:
            self.reqFile.delete("1.0",END)
            req = filename.read()
            self.reqFile.insert(END, req)
            self.reqFile.mark_set(INSERT, '1.0')
            self.reqFile.focus()
    #
    def saveIniF(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_ini)
        if filename:
            textoutput = self.reqFile.get(0.0, END)
            open(filename, 'w').write(textoutput)
    #
    def show_def_log(self, *args):
        load_d_log = self.Lcat.curselection()
        self.d_log_TXT.delete("1.0",END)
        if 1 == len(load_d_log):
            file_d_log = ','.join([self.Lcat.get(ind) for ind in load_d_log])
            self.d_log_TXT.insert(END, open(r'./SQM/PATH_TRAVERSAL/'+file_d_log+'.txt', 'r').read())
            self.d_log_TXT.mark_set(INSERT, '1.0')
            self.d_log_TXT.focus()
        else:
            self.d_log_TXT.insert(END, u"Default-Log-File-Empty.")

    def vfile(self):
        load_file = self.entryFile.get()
        self.sesTXT.delete("1.0",END)
        load_file = load_file.replace("/", "_")
        load_host = self.readHost()
        try:
            log_size = os.path.getsize("./output/"+load_host+"/files/"+load_file)
            if log_size != 0:
                self.sesTXT.insert(END, open(r"./output/"+load_host+"/files/"+load_file, 'r').read())
                self.sesTXT.mark_set(INSERT, '1.0')
                self.sesTXT.focus()
            else:
                self.sesTXT.insert(END, u"File-Empty. ")
        except (IOError,OSError):
            self.sesTXT.insert(END, u"File-Not-Found.")
        return  self.nRoot.select(tab_id=1)
    # file-read
    def chekFile(self):
        sqlFile = self.chkFile_var.get()
        if sqlFile == "on" :
            file_sql= ' --file-read=%s' % (self.entryFile.get())
        else:
            file_sql= ""
        return file_sql
    # File write from:
    def fWFILE(self):
        sqlWFILE = self.varWFILE.get()
        if sqlWFILE == "on":
            filename = tkFileDialog.askopenfile(mode='r',**self.file_WFILE)
            if filename:
                self.eWFILE_var.set(filename.name)
        elif sqlWFILE == "off":
            self.eWFILE_var.set("")
        return
    def readWFILE(self):
        WFILE = self.eWFILE_var.get()
        if WFILE != "":
            sql_WFILE = " --file-write=%s" % WFILE
        else:
            sql_WFILE = ""
        return sql_WFILE
    #File write to:
    def fDFILE(self):
        sqlDFILE = self.chkDFILE_var.get()
        if sqlDFILE == "on" :
            DFILE_sql= ' --file-dest=%s' % (self.eDFILE.get())
        else:
            DFILE_sql= ""
        return DFILE_sql
    #--os-cmd=OSCMD      Execute an operating system command
    def fOSCMD(self):
        sqlOSCMD = self.chkOSCMD_var.get()
        if sqlOSCMD == "on" :
            OSCMD_sql= ' --os-cmd=%s' % (self.eOSCMD.get())
        else:
            OSCMD_sql= ""
        return OSCMD_sql
    #--os-shell          Prompt for an interactive operating system shell
    def fShell(self):
        sqlShell = self.chkShell_var.get()
        if sqlShell == "on" :
            Shell_sql= ' --os-shell'
        else:
            Shell_sql= ""
        return Shell_sql
    #--os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
    def fPWN(self):
        sqlPWN = self.chkPWN_var.get()
        if sqlPWN == "on" :
            PWN_sql= ' --os-pwn'
        else:
            PWN_sql= ""
        return PWN_sql
    #--os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
    def fSmbrelay(self):
        sqlSmbrelay = self.chkSmbrelay_var.get()
        if sqlSmbrelay == "on" :
            Smbrelay_sql= ' --os-smbrelay'
        else:
            Smbrelay_sql= ""
        return Smbrelay_sql
    #--os-bof            Stored procedure buffer overflow exploitation
    def fBOF(self):
        sqlBOF = self.chkBOF_var.get()
        if sqlBOF == "on" :
            BOF_sql= ' --os-bof'
        else:
            BOF_sql= ""
        return BOF_sql
    #--priv-esc          Database process' user privilege escalation
    def fPrivEsc(self):
        sqlPrivEsc = self.chkPrivEsc_var.get()
        if sqlPrivEsc == "on" :
            PrivEsc_sql= ' --priv-esc'
        else:
            PrivEsc_sql= ""
        return PrivEsc_sql
    #--msf-path=MSFPATH  Local path where Metasploit Framework is installed
    def fMSFPATH(self):
        sqlMSFPATH = self.chkMSFPATH_var.get()
        if sqlMSFPATH == "on":
            MSFPATH = tkFileDialog.askdirectory()
            if MSFPATH:
                self.eMSFPATH_var.set(MSFPATH)
        elif sqlMSFPATH == "off":
            self.eMSFPATH_var.set("")
        return
    def rMSFPATH(self):
        sqlMSFPATH = self.chkMSFPATH_var.get()
        if sqlMSFPATH == "on" :
            MSFPATH_sql= ' --msf-path=%s' % (self.eMSFPATH.get())
        else:
            MSFPATH_sql= ""
        return MSFPATH_sql
    #--tmp-path=TMPPATH  Remote absolute path of temporary files directory
    def fTMPPATH(self):
        sqlTMPPATH = self.chkTMPPATH_var.get()
        if sqlTMPPATH == "on" :
            TMPPATH_sql= ' --tmp-path=%s' % (self.eTMPPATH.get())
        else:
            TMPPATH_sql= ""
        return TMPPATH_sql
    #--reg-read          Read a Windows registry key value
    def fRegRead(self):
        sqlRegRead = self.chkRegRead_var.get()
        if sqlRegRead == "on" :
            RegRead_sql= ' --reg-read'
        else:
            RegRead_sql= ""
        return RegRead_sql
    #--reg-add           Write a Windows registry key value data
    def fRegAdd(self):
        sqlRegAdd = self.chkRegAdd_var.get()
        if sqlRegAdd == "on" :
            RegAdd_sql= ' --reg-add'
        else:
            RegAdd_sql= ""
        return RegAdd_sql
    #--reg-del           Delete a Windows registry key value
    def fRegDel(self):
        sqlRegDel = self.chkRegDel_var.get()
        if sqlRegDel == "on" :
            RegDel_sql= ' --reg-del'
        else:
            RegDel_sql= ""
        return RegDel_sql
    #--reg-key=REGKEY    Windows registry key
    def fREGKEY(self):
        sqlREGKEY = self.chkREGKEY_var.get()
        if sqlREGKEY == "on" :
            REGKEY_sql= ' --reg-key=%s' % (self.eREGKEY.get())
        else:
            REGKEY_sql= ""
        return REGKEY_sql
    #--reg-value=REGVAL  Windows registry key value
    def fREGVAL(self):
        sqlREGVAL = self.chkREGVAL_var.get()
        if sqlREGVAL == "on" :
            REGVAL_sql= ' --reg-value=%s' % (self.eREGVAL.get())
        else:
            REGVAL_sql= ""
        return REGVAL_sql
    #--reg-data=REGDATA  Windows registry key value data
    def fREGDATA(self):
        sqlREGDATA = self.chkREGDATA_var.get()
        if sqlREGDATA == "on" :
            REGDATA_sql= ' --reg-data=%s' % (self.eREGDATA.get())
        else:
            REGDATA_sql= ""
        return REGDATA_sql
    #--reg-type=REGTYPE  Windows registry key value type
    def fREGTYPE(self):
        sqlREGTYPE = self.chkREGTYPE_var.get()
        if sqlREGTYPE == "on" :
            REGTYPE_sql= ' --reg-type=%s' % (self.eREGTYPE.get())
        else:
            REGTYPE_sql= ""
        return REGTYPE_sql
    # sql-query
    def chekQuery(self):
        sqlQuery = self.chkQuery_var.get()
        if sqlQuery == "on" :
            query_sql= ' --sql-query=%s' % (self.entryQuery.get())
        else:
            query_sql= ""
        return query_sql
    # - data
    def chekdata(self):
        sqlData = self.chkdata_var.get()
        if sqlData == "on" :
            data_sql= ' --data=%s' % (self.entryData.get())
        else:
            data_sql= ""
        return data_sql
    #--param-del=PDEL
    def fPDEL(self):
        sqlPDEL = self.chkPDEL_var.get()
        if sqlPDEL == "on" :
            PDEL_sql= ' --param-del=%s' % (self.ePDEL.get())
        else:
            PDEL_sql= ""
        return PDEL_sql
    # -Cookie:
    def chekCook(self):
        sqlCook = self.chkCook_var.get()
        if sqlCook == "on" :
            cook_sql= ' --cookie=%s' % (self.entryCook.get())
        else:
            cook_sql= ""
        return cook_sql
    #--load-cookies=LOC
    def fLoadCookies(self):
        sqlLoadCookies = self.chkLoadCookies_var.get()
        if sqlLoadCookies == "on":
            filename = tkFileDialog.askopenfile(mode='r')
            if filename:
                self.varLoadCookies.set(filename.name)
        elif sqlLoadCookies == "off":
            self.varLoadCookies.set("")
        return
    def readLoadCookies(self):
        LOC = self.varLoadCookies.get()
        if LOC != "":
            sql_LOC = " --load-cookies=%s" % LOC
        else:
            sql_LOC = ""
        return sql_LOC
    #--cookie-urlencode  URL Encode generated cookie injections
    def fCookieUrlencode(self):
        sqlCookieUrlencode = self.chkCookieUrlencode_var.get()
        if sqlCookieUrlencode == "on" :
            CookieUrlencode_sql= ' --cookie-urlencode'
        else:
            CookieUrlencode_sql= ""
        return CookieUrlencode_sql
    #--drop-set-cookie
    def fDropSetCookie(self):
        sqlDropSetCookie = self.chkDropSetCookie_var.get()
        if sqlDropSetCookie == "on" :
            DropSetCookie_sql= ' --drop-set-cookie'
        else:
            DropSetCookie_sql= ""
        return DropSetCookie_sql
    #--user-agent=AGENT  HTTP User-Agent header
    def fUA(self):
        sqlUA = self.chkUA_var.get()
        if sqlUA == "on" :
            UA_sql= ' --user-agent=%s' % (self.eUA.get())
        else:
            UA_sql= ""
        return UA_sql
    #--randomize=RPARAM  Randomly change value for given parameter(s)
    def fRandomize(self):
        sqlRandomize = self.chkRandomize_var.get()
        if sqlRandomize == "on" :
            Randomize_sql= ' --randomize=%s' % (self.eRandomize.get())
        else:
            Randomize_sql= ""
        return Randomize_sql
    #--force-ssl         Force usage of SSL/HTTPS requests
    def fForceSsl(self):
        sqlForceSsl = self.chkForceSsl_var.get()
        if sqlForceSsl == "on" :
            ForceSsl_sql= ' --force-ssl'
        else:
            ForceSsl_sql= ""
        return ForceSsl_sql
    #--random-agent
    def fRandomAg(self):
        sqlRandomAg = self.chkRandomAg_var.get()
        if sqlRandomAg == "on" :
            RandomAg_sql= ' --random-agent'
        else:
            RandomAg_sql= ""
        return RandomAg_sql

    def fPROXY(self):
        sqlPROXY = self.chkPROXY_var.get()
        if sqlPROXY == "on" :
            PROXY_sql= ' --proxy=%s' % (self.ePROXY.get())
        else:
            PROXY_sql= ""
        return PROXY_sql

    def fPCRED(self):
        sqlPCRED = self.chkPCRED_var.get()
        if sqlPCRED == "on" :
            PCRED_sql= ' --proxy-cred=%s' % (self.ePCRED.get())
        else:
            PCRED_sql= ""
        return PCRED_sql
    def fPignore(self):
        sqlPignore = self.chkPignore_var.get()
        if sqlPignore == "on" :
            Pignore_sql= ' --ignore-proxy'
        else:
            Pignore_sql= ""
        return Pignore_sql
    #--host=HOST         HTTP Host header
    def fHost(self):
        sqlHOST = self.chkHOST_var.get()
        if sqlHOST == "on" :
            HOST_sql= ' --host=%s' % (self.eHOST.get())
        else:
            HOST_sql= ""
        return HOST_sql
    #--referer=REFERER   HTTP Referer header
    def fReferer(self):
        sqlReferer = self.chkReferer_var.get()
        if sqlReferer == "on" :
            Referer_sql= ' --referer=%s' % (self.eReferer.get())
        else:
            Referer_sql= ""
        return Referer_sql
    #--headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123")
    def fHeaders(self):
        sqlHeaders = self.chkHeaders_var.get()
        if sqlHeaders == "on" :
            Headers_sql= ' --headers=%s' % (self.eHeaders.get())
        else:
            Headers_sql= ""
        return Headers_sql
    #--auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
    def fATYPE(self):
        sqlATYPE = self.chkATYPE_var.get()
        if sqlATYPE == "on" :
            ATYPE_sql= ' --auth-type=%s' % (self.eATYPE.get())
        else:
            ATYPE_sql= ""
        return ATYPE_sql
    #--auth-cred=ACRED   HTTP authentication credentials (name:password)
    def fACRED(self):
        sqlACRED = self.chkACRED_var.get()
        if sqlACRED == "on" :
            ACRED_sql= ' --auth-cred=%s' % (self.eACRED.get())
        else:
            ACRED_sql= ""
        return ACRED_sql
    #--auth-cert=ACERT   HTTP authentication certificate (key_file,cert_file)
    def fACERT(self):
        sqlACERT = self.chkACERT_var.get()
        if sqlACERT == "on" :
            ACERT_sql= ' --auth-cert=%s' % (self.eACERT.get())
        else:
            ACERT_sql= ""
        return ACERT_sql
    #--delay=DELAY       Delay in seconds between each HTTP request
    def fDELAY(self):
        sqlDELAY = self.chkDELAY_var.get()
        if sqlDELAY == "on" :
            DELAY_sql= ' --delay=%s' % (self.eDELAY.get())
        else:
            DELAY_sql= ""
        return DELAY_sql
    #--timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
    def fTIMEOUT(self):
        sqlTIMEOUT = self.chkTIMEOUT_var.get()
        if sqlTIMEOUT == "on" :
            TIMEOUT_sql= ' --timeout=%s' % (self.eTIMEOUT.get())
        else:
            TIMEOUT_sql= ""
        return TIMEOUT_sql
    #--retries=RETRIES   Retries when the connection timeouts (default 3)
    def fRETRIES(self):
        sqlRETRIES = self.chkRETRIES_var.get()
        if sqlRETRIES == "on" :
            RETRIES_sql= ' --retries=%s' % (self.eRETRIES.get())
        else:
            RETRIES_sql= ""
        return RETRIES_sql
    #--scope=SCOPE       Regexp to filter targets from provided proxy log
    def fSCOPE(self):
        sqlSCOPE = self.chkSCOPE_var.get()
        if sqlSCOPE == "on" :
            SCOPE_sql= ' --scope=%s' % (self.eSCOPE.get())
        else:
            SCOPE_sql= ""
        return SCOPE_sql
    #--safe-url=SAFURL   Url address to visit frequently during testing
    def fSAFURL(self):
        sqlSAFURL = self.chkSAFURL_var.get()
        if sqlSAFURL == "on" :
            SAFURL_sql= ' --safe-url=%s' % (self.eSAFURL.get())
        else:
            SAFURL_sql= ""
        return SAFURL_sql
    #--safe-freq=SAFREQ  Test requests between two visits to a given safe url
    def fSAFREQ(self):
        sqlSAFREQ = self.chkSAFREQ_var.get()
        if sqlSAFREQ == "on" :
            SAFREQ_sql= ' --safe-freq=%s' % (self.eSAFREQ.get())
        else:
            SAFREQ_sql= ""
        return SAFREQ_sql
    #--skip-urlencode
    def fSkipUrlencode(self):
        sqlSkipUrlencode = self.chkSkipUrlencode_var.get()
        if sqlSkipUrlencode == "on" :
            SkipUrlencode_sql= ' --skip-urlencode'
        else:
            SkipUrlencode_sql= ""
        return SkipUrlencode_sql
    #--eval=EVALCODE     Evaluate provided Python code before the request (e.g.
                #"import hashlib;id2=hashlib.md5(id).hexdigest()")
    def fEVALCODE(self):
        sqlEVALCODE = self.chkEVALCODE_var.get()
        if sqlEVALCODE == "on" :
            EVALCODE_sql= ' --eval=%s' % (self.eEVALCODE.get())
        else:
            EVALCODE_sql= ""
        return EVALCODE_sql
    #-Prefix
    def chekPrefix(self):
        sqlPrefix = self.chkPrefix_var.get()
        if sqlPrefix == "on" :
            prefix_sql= ' --prefix=%s' % (self.entryPrefix.get())
        else:
            prefix_sql= ""
        return    prefix_sql
    #-Suffix
    def chekSuffix(self):
        sqlSuffix = self.chkSuffix_var.get()
        if sqlSuffix == "on" :
            suffix_sql= ' --suffix=%s' % (self.entrySuffix.get())
        else:
            suffix_sql= ""
        return suffix_sql
    #--os
    def chekOS(self):
        sqlOS = self.chkOS_var.get()
        if sqlOS == "on" :
            os_sql= ' --os=%s' % (self.entryOS.get())
        else:
            os_sql= ""
        return os_sql
    #--skip
    def chekSkip(self):
        sqlSkip = self.chkSkip_var.get()
        if sqlSkip == "on" :
            skip_sql= ' --skip=%s' % (self.entrySkip.get())
        else:
            skip_sql= ""
        return skip_sql
    #--invalid-logical
    def chekLogical(self):
        sqlLogical = self.chkLogical_var.get()
        if sqlLogical == "on" :
            Logical_sql= " --invalid-logical"
        else:
            Logical_sql= ""
        return Logical_sql
    #--invalid-bignum
    def chekBigNum(self):
        sqlBigNum = self.chkBigNum_var.get()
        if sqlBigNum == "on" :
            BigNum_sql= " --invalid-bignum"
        else:
            BigNum_sql= ""
        return BigNum_sql

    #--no-cast
    def chekCast(self):
        sqlCast = self.chkCast_var.get()
        if sqlCast == "on" :
            cast_sql= " --no-cast"
        else:
            cast_sql= ""
        return cast_sql
    # --string
    def chekStr(self):
        sqlStr = self.chkStr_var.get()
        if sqlStr == "on" :
            str_sql= ' --string=%s' % (self.entryStr.get())
        else:
            str_sql= ""
        return    str_sql
    # --regexp
    def chekReg(self):
        sqlReg = self.chkReg_var.get()
        if sqlReg == "on" :
            reg_sql= ' --regexp=%s' % (self.entryReg.get())
        else:
            reg_sql= ""
        return reg_sql
    # -code
    def chekCode(self):
        sqlCode = self.chkCode_var.get()
        if sqlCode == "on" :
            code_sql= ' --code=%s' % (self.entryCode.get())
        else:
            code_sql= ""
        return code_sql

    # uCols
    def chekCol(self):
        sqlCol = self.chkCol_var.get()
        if sqlCol == "on" :
            col_sql= ' --union-cols=%s' % (self.entryCol.get())
        else:
            col_sql= ""
        return    col_sql
    # uChar
    def chekChar(self):
        sqlChar = self.chkChar_var.get()
        if sqlChar == "on" :
            char_sql= ' --union-char=%s' % (self.entryChar.get())
        else:
            char_sql= ""
        return char_sql
    def chekSec(self):
        sqlSec = self.chkSec_var.get()
        if sqlSec == "on" :
            sec_sql= ' --time-sec=%s' % (self.entrySec.get())
        else:
            sec_sql= ""
        return sec_sql
    # -o
    def chekOpt(self):
        sqlOpt = self.chkOpt_var.get()
        if sqlOpt == "on" :
            opt_sql= " -o"
        else:
            opt_sql= ""
        return opt_sql
    #-o
    def fO(self):
        sqlO = self.chkO_var.get()
        if sqlO == "on" :
            O_sql= " -o"
        else:
            O_sql= ""
        return O_sql
    #--predict-output
    def chekPred(self):
        sqlPred = self.chkPred_var.get()
        if sqlPred == "on" :
            pred_sql= " --predict-output"
        else:
            pred_sql= ""
        return pred_sql
    #--keep-alive
    def chekKeep(self):
        sqlKeep = self.chkKeep_var.get()
        if sqlKeep == "on" :
            keep_sql= " --keep-alive"
        else:
            keep_sql= ""
        return keep_sql
    #--null-connection
    def chekNull(self):
        sqlNull = self.chkNull_var.get()
        if sqlNull == "on" :
            null_sql= " --null-connection"
        else:
            null_sql= ""
        return null_sql
    # text only
    def chekTxt(self):
        sqlTxt = self.chk_Txt_var.get()
        if sqlTxt == "on" :
            txt_sql= " --text-only"
        else:
            txt_sql= ""
        return txt_sql
    # -Title
    def chekTit(self):
        sqlTit = self.chk_Tit_var.get()
        if sqlTit == "on" :
            tit_sql= " --titles"
        else:
            tit_sql= ""
        return tit_sql
    # --batch
    def chekBatch(self):
        sqlBatch = self.chk_Batch_var.get()
        if sqlBatch == "on" :
            batch_sql= " --batch"
        else:
            batch_sql= ""
        return batch_sql
    #--HEX
    def chekHex(self):
        sqlHex = self.chk_Hex_var.get()
        if sqlHex == "on" :
            hex_sql= " --hex"
        else:
            hex_sql= ""
        return hex_sql
    #--save
    def fSave(self):
        sqlSave = self.chk_Save_var.get()
        if sqlSave == "on" :
            Save_sql= " --save"
        else:
            Save_sql= ""
        return Save_sql
    # -b --Banner
    def chekBanner(self):
        sqlBanner = self.chk_Banner_var.get()
        if sqlBanner == "on" :
            banner_sql= " --banner"
        else:
            banner_sql= ""
        return banner_sql

    #-f, --fingerprint
    def chekFing(self):
        sqlFing = self.chk_fing_var.get()
        if sqlFing == "on" :
            fing_sql= " -f"
        else:
            fing_sql= ""
        return fing_sql
    # DBMS
    def chek_dbms(self, *args):
        sql_dbms = self.chk_dbms_var.get()
        if sql_dbms == "on" :
            self.box.config(state = 'readonly')
            sqlDB = " --dbms=%s" % (self.box_value.get())
        else:
            self.box.config(state = 'disabled')
            sqlDB = ""
        return sqlDB
    #-p
    def chekParam(self):
        sqlParam = self.chkParam_var.get()
        if sqlParam == "on" :
            param_sql= ' -p %s' % (self.entryParam.get())
        else:
            param_sql= ""
        return    param_sql
    #Level
    def chek_level(self, *args):
        sql_level= self.chk_level_var.get()
        if sql_level == "on" :
            self.box_level.config(state = 'readonly')
            level_sql = " --level=%s" % (self.box_level_value.get())
        else:
            self.box_level.config(state = 'disabled')
            level_sql = ""
        return level_sql
    # Risk
    def chek_risk(self, *args):
        sql_risk= self.chk_risk_var.get()
        if sql_risk == "on" :
            self.box_risk.config(state = 'readonly')
            risk_sql = " --risk=%s" % (self.box_risk_value.get())
        else:
            self.box_risk.config(state = 'disabled')
            risk_sql = ""
        return risk_sql
    # VERBOSE LEVEL Func
    def chek_verb(self, *args):
        sql_verb= self.chk_verb_var.get()
        if sql_verb == "on" :
            self.box_verb.config(state = 'readonly')
            verb_sql = " -v %s" % (self.box_verb_value.get())
        else:
            self.box_verb.config(state = 'disabled')
            verb_sql = ""
        return verb_sql
    # Threads chek_thr
    def chek_thr(self, *args):
        sql_thr= self.chk_thr_var.get()
        if sql_thr == "on" :
            self.thr.config(state = 'normal')
            thr_sql = ' --threads=%s' % (self.thr_value.get())
        else:
            self.thr.config(state = 'disabled')
            thr_sql = ""
        return thr_sql
    # Tec
    def chek_tech(self, *args):
        sql_tech= self.chk_tech_var.get()
        if sql_tech == "on" :
            self.boxInj.config(state = 'normal')
            tech_sql= " --technique=%s" % (self.boxInj_value.get())
        else:
            self.boxInj.config(state = 'disabled')
            tech_sql = ""
        return tech_sql
    #--dns-domain=
    def chekDNS(self,*args):
        sql_dns= self.chkDNS_var.get()
        if sql_dns == "on" :
            dns_sql= ' --dns-domain=%s' % (self.entryDNS.get())
        else:
            dns_sql = ""
        return dns_sql

    # tamper
    def chek_tam(self, *args):
        sel = self.Ltamper.curselection()
        if 0 < len(sel):
            tam_sql= " --tamper %s" % (",".join([self.Ltamper.get(x) for x in sel]))
        else:
            tam_sql = ""
        return tam_sql
    #
    def readHost(self):
        selection = self.varTarget.get()
        fileR =  self.urlentry.get()
        if selection == "requestFile":
            load_host = ""
            text = [line.rstrip() for line in open(fileR) if len(line) > 2]
            for x in text:
                if "Host" in x:
                    load_host = x.replace("Host: ","")
            if load_host == "":
                load_host = "Invalid requestFile :("
        else:
            load_url = self.urlentry.get()
            load_host = urlparse(load_url).netloc
        return load_host
    # log viewer
    def sqlmap(self, *args):
        load_host = self.readHost()
        #print load_host
        text = open(r"./output/"+load_host+"/log", 'r').readlines()
        pattern = re.compile(r'(?m)(^sqlmap(.*)|^---$|^Place:(.*)|^Parameter:(.*)|\s{4,}Type:(.*)|\s{4,}Title:(.*)|\s{4,}Payload:(.*)|\s{4,}Vector:(.*))$', re.DOTALL)
        mode = os.O_CREAT | os.O_TRUNC
        f = os.open(r"./output/"+load_host+"/gui_log", mode)
        os.close(f)
        for x in text:
            qq = pattern.sub('', x).strip("\n")
            if len(qq) > 4:
                mode = os.O_WRONLY | os.O_APPEND
                f = os.open(r"./output/"+load_host+"/gui_log", mode)
                os.write(f,qq+'\n')
                os.close(f)
    # load log whitout query
    #self.chkLog_var whith query
    def logs(self, *args):
        logfile = ""
        if self.chkLog_var.get() == "on":
            logfile = "log"
        else:
            logfile = "gui_log"

        load_host = self.readHost()
        #print load_host
        self.sesTXT.delete("1.0",END)
        # highlight it
        s = ['available databases', 'Database:', 'Table:', '[*]',
             'database management system users:','current user:',
             'database management system users', 'password hashes:',
             'password hash:','found databases','file saved to:',
             ]
        try:
            log_size = os.path.getsize("./output/"+load_host+"/log")
            if log_size != 0:
                self.sqlmap()
                #
                self.sesTXT.insert(END,open(("./output/%s/%s" % (load_host,logfile)), 'r').read())
                self.sesTXT.mark_set(INSERT, '1.0')
                for tagz in s:
                    idx = '1.0'
                    while 1:
                        idx = self.sesTXT.search(tagz, idx, nocase=1, stopindex=END)
                        if not idx: break
                        lastidx = '%s+%dc' % (idx, len(tagz))
                        self.sesTXT.tag_add('found', idx, lastidx)
                        idx = lastidx
                        self.sesTXT.tag_config('found',font=('arial', 8,'bold'))
                        self.sesTXT.focus()
            else:
                self.sesTXT.insert(END, u"Log-Empty "+load_host+".")
        except (IOError,OSError):
            self.sesTXT.insert(END, u"Log-Not-Found "+load_host+".")
        return
    # Show current session
    def session(self):
        load_host = self.readHost()
        self.sesTXT.delete("1.0",END)
        try:
            session_size = os.path.getsize("./output/"+load_host+"/session")
            if session_size != 0:
                self.sesTXT.insert(END, open(r"./output/"+load_host+"/session", 'r').read())
                self.sesTXT.mark_set(INSERT, '1.0')
                self.sesTXT.focus()
            else:
                self.sesTXT.insert(END, u"Session-File-Empty "+load_host+".")
        except (IOError,OSError):
            self.sesTXT.insert(END, u"Session-File-Not-Found "+load_host+".")
        return
    # cur-t user
    def chekCurrent_user(self):
        sqlCurrent_user = self.chkCurrent_user_var.get()
        if sqlCurrent_user == "on" :
            current_user_sql= " --current-user"
        else:
            current_user_sql= ""
        return current_user_sql
    # cur-t db:
    def chekCurrent_db(self):
        sqlCurrent_db = self.chkCurrent_db_var.get()
        if sqlCurrent_db == "on" :
            current_db_sql= " --current-db"
        else:
            current_db_sql= ""
        return current_db_sql
    # dba
    def chek_is_dba(self):
        sql_is_dba = self.chk_is_dba_var.get()
        if sql_is_dba == "on" :
            is_dba_sql= " --is-dba"
        else:
            is_dba_sql= ""
        return is_dba_sql
    # users
    def chek_users(self):
        sql_users = self.chk_users_var.get()
        if sql_users == "on" :
            users_sql= " --users"
        else:
            users_sql= ""
        return users_sql
    # pas
    def chek_passwords(self):
        sql_passwords = self.chk_passwords_var.get()
        if sql_passwords == "on" :
            passwords_sql= " --passwords"
        else:
            passwords_sql= ''
        return passwords_sql
    # priv
    def chek_privileges(self):
        sql_privileges = self.chk_privileges_var.get()
        if sql_privileges == "on" :
            privileges_sql= " --privileges"
        else:
            privileges_sql= ""
        return privileges_sql
    # roles
    def chek_roles(self):
        sql_roles = self.chk_roles_var.get()
        if sql_roles == "on" :
            roles_sql= " --roles"
        else:
            roles_sql= ""
        return roles_sql
    #--common-tables     Check existence of common tables
    def chekBFt(self):
        sql_BFt = self.chkBFt_var.get()
        if sql_BFt == "on" :
            BFt_sql= " --common-tables"
        else:
            BFt_sql= ""
        return BFt_sql
    #--common-columns     Check existence of common columns
    def chekBFc(self):
        sql_BFc = self.chkBFc_var.get()
        if sql_BFc == "on" :
            BFc_sql= " --common-columns"
        else:
            BFc_sql= ""
        return BFc_sql
    # dbs
    def chek_dbs(self):
        sql_dbs = self.chk_dbs_var.get()
        if sql_dbs == "on" :
            dbs_sql= " --dbs"
        else:
            dbs_sql= ""
        return dbs_sql
    # tbl
    def chek_tables(self):
        sql_tables = self.chk_tables_var.get()
        if sql_tables == "on" :
            tables_sql= " --tables"
        else:
            tables_sql= ""
        return tables_sql
    # clmn
    def chek_columns(self):
        sql_columns = self.chk_columns_var.get()
        if sql_columns == "on" :
            columns_sql= " --columns"
        else:
            columns_sql= ""
        return columns_sql
    # schema
    def chek_schema(self):
        sql_schema = self.chk_schema_var.get()
        if sql_schema == "on" :
            schema_sql= " --schema"
        else:
            schema_sql= ""
        return schema_sql
    # count
    def chek_count(self):
        sql_count = self.chk_count_var.get()
        if sql_count == "on" :
            count_sql= " --count"
        else:
            count_sql= ""
        return count_sql
    # --dump
    def chek_dump(self):
        sql_dump = self.chk_dump_var.get()
        if sql_dump == "on" :
            dump_sql= " --dump"
        else:
            dump_sql= ""
        return dump_sql
    # --dump-all
    def chek_dump_all(self):
        sql_dump_all = self.chk_dump_all_var.get()
        if sql_dump_all == "on" :
            dump_all_sql= " --dump-all"
        else:
            dump_all_sql= ""
        return dump_all_sql
    # --dump-all
    def chek_exclude(self):
        sql_exclude = self.chk_exclude_var.get()
        if sql_exclude == "on" :
            exclude_sql= " --exclude-sysdbs"
        else:
            exclude_sql= ""
        return exclude_sql
    # --search
    def chek_search(self):
        sql_search = self.chk_search_var.get()
        if sql_search == "on" :
            search_sql= " --search"
        else:
            search_sql= ""
        return search_sql
    # -D
    def chekD(self,*args):
        sqlD = self.chkD_var.get()
        if sqlD == "on" :
            D_sql= ' -D %s' % (self.entryD.get())
        else:
            D_sql= ""
        return    D_sql
    #-T TBL
    def chekT(self,*args):
        sqlT = self.chkT_var.get()
        if sqlT == "on" :
            T_sql= ' -T %s' % (self.entryT.get())
        else:
            T_sql= ""
        return    T_sql
    #-C COL
    def chekC(self,*args):
        sqlC = self.chkC_var.get()
        if sqlC == "on" :
            C_sql= ' -C %s' % (self.entryC.get())
        else:
            C_sql= ""
        return    C_sql
    #-U USER
    def fUSER(self):
        sqlU = self.chkUSER_var.get()
        if sqlU == "on" :
            U_sql= ' -U %s' % (self.eUSER.get())
        else:
            U_sql= ""
        return U_sql
    # --start --stop limit
    def chek_start_stop(self,*args):
        try:
            sql_start = self.chk_start_var.get()
            if sql_start == "on" :
                param = self.entry_start.get()
                start = param.split(',')[0]
                stop = param.split(',')[1]
                start_sql= ' --start=%s --stop=%s' % (start,stop)
            else:
                start_sql= ""
            return start_sql
        except:
            pass
    #--sql-shell
    def fSqlShell(self):
        SqlShell = self.chkSqlShell_var.get()
        if SqlShell == "on" :
            Sql_Shell= ' --sql-shell'
        else:
            Sql_Shell= ""
        return Sql_Shell
    # --first limit
    def chek_first(self,*args):
        sql_first= self.chk_first_var.get()
        if sql_first == "on" :
            first_sql= ' --first=%s' % (self.entry_first.get())
        else:
            first_sql= ""
        return first_sql
    # --last limit
    def chek_last(self,*args):
        sql_last = self.chk_last_var.get()
        if sql_last == "on" :
            last_sql= ' --last=%s' % (self.entry_last.get())
        else:
            last_sql= ""
        return last_sql
    #--check-tor
    def fTor(self):
        sql_Tor = self.chkTor_var.get()
        if sql_Tor == "on" :
            tor_sql= ' --check-tor'
        else:
            tor_sql= ''
        return tor_sql
    # --tor
    def fTorUse(self):
        sql_TorUse = self.chkTorUse_var.get()
        if sql_TorUse == "on" :
            TorUse_sql= ' --tor'
        else:
            TorUse_sql= ''
        return TorUse_sql
    # --tor-port=TORPORT  Set Tor proxy port other than default
    def fTorPort(self,*args):
        sql_TorPort = self.chkTorPort_var.get()
        if sql_TorPort == "on" :
            TorPort_sql= ' --tor-port=%s' % (self.eTorPort.get())
        else:
            TorPort_sql= ""
        return TorPort_sql
    #--tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
    def fTorType(self,*args):
        sql_TorType = self.chkTorType_var.get()
        if sql_TorType == "on" :
            TorType_sql= ' --tor-type=%s' % (self.eTorType.get())
        else:
            TorType_sql= ""
        return TorType_sql
    #--eta
    def fEta(self):
        sql_Eta = self.chkEta_var.get()
        if sql_Eta == "on" :
            Eta_sql= ' --eta'
        else:
            Eta_sql= ''
        return Eta_sql
    #--forms
    def fForms(self):
        sql_Forms = self.chkForms_var.get()
        if sql_Forms == "on" :
            Forms_sql= ' --forms'
        else:
            Forms_sql= ''
        return Forms_sql
    #--fresh-queries
    def fFresh(self):
        sql_Fresh = self.chkFresh_var.get()
        if sql_Fresh == "on" :
            Fresh_sql= ' --fresh-queries'
        else:
            Fresh_sql= ''
        return Fresh_sql
    #--parse-errors
    def fParseEr(self):
        sql_ParseEr = self.chkParseEr_var.get()
        if sql_ParseEr == "on" :
            ParseEr_sql= ' --parse-errors'
        else:
            ParseEr_sql= ''
        return ParseEr_sql
    #--flush-session
    def fFlush(self):
        sql_Flush = self.chkFlush_var.get()
        if sql_Flush == "on" :
            Flush_sql= ' --flush-session'
        else:
            Flush_sql= ''
        return Flush_sql
    #--charset=CHARSET   Force character encoding used for data retrieval
    def fCharset(self,*args):
        sql_Charset = self.chkCharset_var.get()
        if sql_Charset == "on" :
            Charset_sql= ' --charset=%s' % (self.eCharset.get())
        else:
            Charset_sql= ""
        return Charset_sql
    #--crawl=CRAWLDEPTH  Crawl the website starting from the target url
    def fCrawl(self,*args):
        sql_Crawl = self.chkCrawl_var.get()
        if sql_Crawl == "on" :
            Crawl_sql= ' --crawl=%s' % (self.eCrawl.get())
        else:
            Crawl_sql= ""
        return Crawl_sql
    #--csv-del=CSVDEL
    def fCsv(self,*args):
        sql_Csv = self.chkCsv_var.get()
        if sql_Csv == "on" :
            Csv_sql= ' --csv-del=%s' % (self.eCsv.get())
        else:
            Csv_sql= ""
        return Csv_sql
    #--output-dir=ODIR
    def fOutDir(self):
        sql_OutDir = self.chkOutDir_var.get()
        if sql_OutDir == "on" :
            OutDir_sql= ' --output-dir=%s' % (self.eOutDir.get())
        else:
            OutDir_sql= ""
        return OutDir_sql
    #--dbms-cred=DCRED
    def fDCRED(self):
        sql_DCRED = self.chkDCRED_var.get()
        if sql_DCRED == "on" :
            DCRED_sql= ' --dbms-cred=%s' % (self.eDCRED.get())
        else:
            DCRED_sql= ""
        return DCRED_sql
    #--replicate
    def fReplicate(self,*args):
        sql_Replicate = self.chkReplicate_var.get()
        if sql_Replicate == "on" :
            Replicate_sql= ' --replicate'
        else:
            Replicate_sql= ''
        return Replicate_sql
    # sqlmap:
    def commands(self,*args):
        selection = self.varTarget.get()
        tag = self.urlentry.get()
        if selection == "url":
            target = ' --url="%s"' % (tag)
        elif selection == "logFile":
            target = ' -l %s' % (tag)
        elif selection == "bulkFile":
            target = ' -m %s' % (tag)
        elif selection == "requestFile":
            target = ' -r %s' % (tag)
        elif selection == "googleDork":
            target = ' -g %s' % (tag)
            z_param = ""
        elif selection == "direct":
            target = ' -d %s' % (tag)
        elif selection == "configFile":
            target = ' -c %s' % (tag)
        #
        try:
            inject = target+self.chekParam()+self.chek_tam()+ \
                self.readWFILE()+self.fDFILE()+self.rMSFPATH()+ \
                self.fOSCMD()+self.fShell()+self.fPWN()+self.fSmbrelay()+self.fBOF()+ \
                self.fPrivEsc()+self.fTMPPATH()+self.chekFile()+self.fOutDir()+ \
                self.fRegRead()+self.fRegAdd()+self.fRegDel()+self.fREGKEY()+ \
                self.fREGVAL()+self.fREGDATA()+self.fREGTYPE()+self.chekQuery()+ \
                self.chekdata()+self.fPDEL()+self.fRandomAg()+self.fPROXY()+ \
                self.fPCRED()+self.fPignore()+self.chek_level()+self.chek_risk()+ \
                self.chekTit()+self.chekHex()+self.chekTxt()+self.chekCode()+ \
                self.chekReg()+self.chekStr()+self.chekSec()+self.chek_tech()+ \
                self.chekDNS()+self.chekOpt()+self.fO()+self.chekPred()+self.chekKeep()+ \
                self.chekNull()+self.chek_thr()+self.chek_dbms()+self.chekCol()+ \
                self.chekChar()+self.chekCook()+ self.readLoadCookies()+ \
                self.fCookieUrlencode()+self.fDropSetCookie()+self.chekPrefix()+ \
                self.fUA()+self.fRandomize()+self.fForceSsl()+self.fHost()+self.fReferer()+ \
                self.fHeaders()+self.fACERT()+self.fACRED()+self.fATYPE()+ \
                self.fDELAY()+self.fTIMEOUT()+self.fRETRIES()+self.fSCOPE()+ \
                self.fSAFURL()+self.fSAFREQ()+self.fSkipUrlencode()+self.fEVALCODE()+ \
                self.chekSuffix()+self.chekOS()+self.chekSkip()+self.chekBigNum()+self.chekLogical()+ \
                self.chekCast()+self.chekBatch()+self.chekCurrent_user()+self.chekCurrent_db()+ \
                self.chek_is_dba()+self.chek_users()+self.chek_passwords()+self.fDCRED()+ \
                self.chek_privileges()+self.chek_roles()+self.chek_dbs()+self.chekBFt()+self.chekBFc()+ \
                self.chek_tables()+self.chek_columns()+self.chek_schema()+ \
                self.chek_count()+self.chek_dump()+self.chek_dump_all()+ \
                self.chek_search()+self.chekD()+self.chekT()+self.chekC()+self.fUSER()+ \
                self.chek_exclude()+self.chek_start_stop()+self.chek_first()+ \
                self.chek_last()+self.chek_verb()+self.fSqlShell()+self.fDLike()+self.fDHash()+ \
                self.chekFing()+self.chekBanner()+self.fTor()+self.fTorUse()+ \
                self.fTorPort()+self.fTorType()+self.fEta()+self.fForms()+ \
                self.fFresh()+self.fParseEr()+self.fFlush()+self.fCharset()+ \
                self.fCrawl()+self.fCsv()+self.fReplicate()+ self.fTrafFile()+ \
                self.fSesFile()+self.fSave()+self.fBeep()+self.fPayload()+ \
                self.fWaf()+self.fCleanup()+self.fDependencies()+self.fGpage()+self.fTSTF()+ \
                self.fExact()+self.fMobile()+self.fRank()+self.fPurge()+self.fSmart()
        except:
            inject = "select target :)"
        finally:
            self.sql_var.set(inject)
    # GOGO!!!
    def injectIT(self,*args):
        if (os.name == "posix"):
            #cmd = "YourFavoriteTerminal -h -e python sqlmap.py %s" % (self.sqlEdit.get())
            cmd = "sakura -h -e python2 sqlmap.py %s" % (self.sqlEdit.get())
        else:
            cmd = "start cmd /k python sqlmap.py %s" % (self.sqlEdit.get())
        #Write last target [last 50 test]

        mode = os.O_TRUNC | os.O_WRONLY
        fwr = os.open(r"./SQM/last.uri", mode)
        os.write(fwr,self.urlentry.get())
        os.close(fwr)
        subprocess.Popen(cmd, shell = True)
    # CopyPasteCut
    def rClicker(self, e):
        try:
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')

            def rClick_Cut(e):
                e.widget.event_generate('<Control-x>')

            def rClick_Paste(e):
                e.widget.event_generate('<Control-v>')

            e.widget.focus()
            nclst=[
                (' Cut', lambda e=e: rClick_Cut(e)),
                (' Copy', lambda e=e: rClick_Copy(e)),
                (' Paste', lambda e=e: rClick_Paste(e)),
            ]
            rmenu = Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        except TclError:
            pass
        return "break"

    def rClickbinder(self):
        try:
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']:
                self.bind_class(b, sequence='<Button-3>', func = self.rClicker, add='')
        except TclError:
            pass

    def onFind(self,*args):
        target = self.searchEdit.get()
        if target:
            where = self.sesTXT.search(target, INSERT, END)  # from insert cursor
            if where:                                      # returns an index
                pastit = where + ('+%dc' % len(target))    # index past target
                self.sesTXT.tag_remove('foo', '1.0', END)      # remove selection
                self.sesTXT.tag_add('foo', where, pastit)      # select found target
                self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8,'bold') )
                self.sesTXT.mark_set(INSERT, pastit)         # set insert mark
                self.sesTXT.see(INSERT)                      # scroll display
                self.sesTXT.focus()                          # select text widget
            else:
                self.sesTXT.mark_set(INSERT, '1.0')
                self.sesTXT.tag_remove('foo', '1.0', END)      # remove selection
                self.sesTXT.tag_config('foo', foreground='yellow')
                self.sesTXT.focus()

    def onFindAll(self,*args):
        target = self.searchEdit.get()
        self.sesTXT.mark_set(INSERT, '1.0')
        self.sesTXT.tag_remove('foo', '1.0', END)      # remove selection
        self.sesTXT.focus()
        if target:
            while 1:
                where = self.sesTXT.search(target, INSERT, END)

                if where:
                    pastit = where + ('+%dc' % len(target))
                    self.sesTXT.tag_add('foo', where, pastit)
                    self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8,'bold'))
                    self.sesTXT.mark_set(INSERT, pastit)
                    self.sesTXT.see(INSERT)
                    self.sesTXT.focus()
                else:
                    break
    # Hotkey Alt + 1 2 3 4 5
    def alt_key_1(self,*args):
        return self.noBF.select(tab_id=0)
    def alt_key_2(self,*args):
        return self.noBF.select(tab_id=1)
    def alt_key_3(self,*args):
        return self.noBF.select(tab_id=2)
    def alt_key_4(self,*args):
        return self.noBF.select(tab_id=3)
    def alt_key_5(self,*args):
        return self.noBF.select(tab_id=4)
    #s l e h
    def alt_key_s(self,*args):
        return self.nRoot.select(tab_id=0)
    def alt_key_l(self,*args):
        return self.nRoot.select(tab_id=1)
    def alt_key_e(self,*args):
        return self.nRoot.select(tab_id=2)
    def Help_F1(self,*args):
        return self.nRoot.select(tab_id=3)
#-----------------------------------------
def main():
    root = Tk()
    f = tkFont.Font(family='Simsun', size= 10)
    s = ttk.Style()
    s.theme_use('clam')
    s.configure('.', font=f)
    root.title('SQLmap Command Builder')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(True, True)
    appl = app(mw=root)
    appl.mainloop()
#-----------------------------------------
if __name__ == '__main__':
    main()