# -*- coding: utf-8 -*-

"""
first_tier_city = ['北京','上海','广州','深圳']  # 上海
new_first_tier_city = ['成都','重庆','杭州','西安','武汉','苏州','郑州','南京','天津','长沙','东莞','宁波','佛山','合肥','青岛']    # 重庆
second_tier_city = ['昆明','沈阳','济南','无锡','厦门','温州','哈尔滨','大连','贵阳','南宁','石家庄','长春','南昌','太原','珠海']     # 无锡
"""

"""
城市选择: 以2023年第一季度GDP排名为依据, 分别选取一线、新一线、二线城市中的第一名的部分职业的招聘数据做分析
"""

data_city = {'上海': '101020100', '重庆': '101040100', '无锡': '101190200'}


data_position = {'_NET': '100107', '语音视频图形开发': '100121', 'AI训练师': '130121', 'Java': '100101', 'PHP': '100103', 'Python': '100109','Golang': '100116','Hadoop': '100108', '数据采集': '100122', 'GIS工程师': '100124', '全栈工程师': '100123','前端开发工程师': '100901', 'Android': '100202', 'iOS': '100203', 'UthreeD': '100209','UEfour': '100211', 'Cocos': '100210',  '技术美术': '100212', 'JavaScript': '100208', '软件测试': '100309','自动化测试': '100302', '功能测试': '100303', '测试开发': '100305', '硬件测试': '100308', '游戏测试': '100307', '性能测试': '100304', '渗透测试': '100310', '移动端测试': '100306', '运维工程师': '100401', 'IT技术支持': '100405', '网络工程师': '100403','网络安全': '100407', '系统工程师': '100404', '运维开发工程师': '100402','系统管理员': '100406', 'DBA': '100409', '系统安全': '100408', '技术文档工程师': '100410', '图像算法': '101306', '自然语言处理算法': '100117','大模型算法': '101310', '数据挖掘': '100104', '规控算法': '101311', 'SLAM算法': '101312', '推荐算法': '100118', '搜索算法': '100115', '语音算法': '101305', '风控算法': '101309','算法工程师': '100120', '机器学习': '101301', '深度学习': '101302', '自动驾驶系统工程师': '101308', '数据分析师': '260102', '数据开发': '100508', '数据仓库': '100507', 'ETL工程师': '100506', '数据架构师': '100512', '实施工程师': '100606', '需求分析工程师': '100607', '架构师': '100704', '电气工程师': '101402', '电子工程师': '101401', '电气设计工程师': '101404', '集成电路IC设计': '101405', 'IC验证工程师': '101406', '版图设计工程师': '101407', 'FAE': '101403', '电子维修技术员': '101408', '硬件工程师': '100801', '嵌入式': '100802', '自动化': '100803', 'FPGA开发': '100808', '单片机': '100804', '驱动开发': '100806', 'PCB工艺': '100811', '射频工程师': '100816', '电路设计': '100805', '系统集成': '100807', '光学工程师': '100818', 'DSP开发': '100809', 'ARM开发': '100810',  '通信技术工程师': '101001', '通信研发工程师': '101002', '移动通信工程师': '101004', '电信网络工程师': '101005', '数据通信工程师': '101003', '通信测试工程师': '101014', '光通信工程师': '101016', '光传输工程师': '101017', '光网络工程师': '101018', '通信电源工程师': '101009', '有线传输工程师': '101007', '通信设备工程师': '101015', '核心网工程师': '101013', '通信标准化工程师': '101010', '电信交换工程师': '101006', '电商产品经理': '110106', '数据产品经理': '110105', '移动产品经理': '110103', 'AI产品经理': '110110', '游戏策划': '110107', '系统策划': '120305', '游戏数值策划': '120303', '游戏制作人': '110303', '金融产品经理': '180501', '硬件产品经理': '110109', '化妆品产品经理': '110111','客服专员': '130305','网络客服': '130303', '电话客服': '130308', '新媒体运营': '130111', '直播运营': '130122', '视频运营': '170108', '内容运营': '130104', '微信运营': '130113', '国内电商运营': '130117', '跨境电商运营': '130124', '品类运营': '130107', '淘宝运营': '130126', '天猫运营': '130127', '京东运营': '130128', '拼多多运营': '130129', '亚马逊运营': '130130', '阿里国际站运营': '130132', '产品运营': '130102', '用户运营': '130101', '商家运营': '130106', '社区运营': '130112', '游戏运营': '130108', '活动运营': '130105', '网站运营': '130110', '内容审核': '130120', '车辆运营': '130123', '线下拓展运营': '130116', '商场运营': '290314', '文案编辑': '130203', '网站编辑': '130204', '医学编辑': '210101', '销售专员': '140301', '电话销售': '140310', '网络销售': '140314', '渠道销售': '140307', '客户代表': '140303', '销售工程师': '140316', '销售运营': '130119', '商务专员': '160301', '外贸业务员': '250203', '课程顾问': '190601', '招生顾问': '190602', '留学顾问': '190603', '汽车销售': '230201', '汽车配件销售': '230202','置业顾问': '160401', '地产中介': '160403', '物业招商管理': '220403',  '服装导购': '160501', '珠宝销售': '290312', '美容顾问': '210414', '化妆品导购': '210406', '会籍顾问': '210610', '瘦身顾问': '210602', '旅游顾问': '280103', '医药代表': '210502', '医疗器械销售': '210506', '药店店员': '210803', '药店店长': '210801', '医美咨询': '210505', '健康顾问': '210504', '口腔咨询师': '210507', '广告销售': '140313', '证券经纪人': '180801', '前台': '150202', '后勤': '150207', '经理助理': '150205', '文员': '150210', '企业党建': '140802', '招聘': '150102', 'HRBP': '150103', '培训': '150105', '员工关系': '150109', '组织发展': '150110', '企业文化': '150111', '薪酬绩效': '150106', '法务总监': '150507', '法律顾问': '150504', '律师': '150502', '会计': '150301', '总账会计': '150311', '成本会计': '150310', '结算会计': '150304', '税务外勤会计': '150313', '审计': '150306', '税务': '150305', '出纳': '150302', '风控': '150307', '财务顾问': '150303', '统计员': '150314', '质检员': '300208', '实验室技术员': '300402', '体系工程师': '300205', '体系审核员': '300206', '产品认证工程师': '300204', '失效分析工程师': '300203', '可靠度工程师': '300202', '汽车质量工程师': '230109', '计量工程师': '300209', '机械工程师': '300301',  '工艺工程师': '300308',  '模具工程师': '300314', '机械制图员': '300305', '机电工程师': '300310', '注塑工程师': '300316', '夹具工程师': '300313', '冲压工程师': '300312', '材料工程师': '300309', '工业工程师': '300307', '焊接工程师': '300315', '热设计工程师': '100813', '液压工程师': '300318', '生产文员': '300108', '生产设备管理员': '300106', '厂务': '300110', '生产安全员': '300207', '施工安全员': '220225', 'EHS工程师': '300903', '安全评价师': '300210', '化工工程师': '300401', '化妆品研发': '300405', '涂料研发': '300404', '化工项目经理': '300407', '电池工程师': '300801', '电机工程师': '300802', '汽车电子工程师': '230106', '线束设计': '300803', '内外饰设计工程师': '230110', '动力系统工程师': '230105', '底盘工程师': '230103', '汽车零部件设计': '230107', '汽车设计': '230101', '总装工程师': '230210', '汽车项目管理': '230108', '环境检测员': '300905', '环保工程师': '300901', '碳排放管理师': '300904','收银': '290201', '导购': '290302', '门店店长': '290304', '美容师': '210405', '美容店长': '210410', '美体师': '210408', '美甲师': '210608', '美睫师': '210413', '纹绣师': '210407', '发型师': '210607', '养发师': '290801', '理疗师': '210403', '针灸推拿': '210404', '按摩师': '210412', '足疗师': '210411', '采耳师': '210415', '保安': '290105', '消防中控员': '290121', '押运员': '290120', '安检员': '290112', '保洁': '290106', '保洁经理': '290122', '保姆': '290108', '月嫂': '290109', '产后康复师': '290118', '育婴师': '290110', '护工': '290111', '家电维修': '290114', '手机维修': '290113', '电脑维修': '290166', '汽车维修': '230204', '汽车美容': '230205', '洗车工': '230213', '加油员': '230214', '宠物美容': '290601', '宠物医生': '290602', '健身教练': '190705', '舞蹈老师': '190701', '瑜伽老师': '190702', '救生员': '210613', '游泳教练': '190704', '网约车司机': '240305', '代驾司机': '240306', '驾校教练': '240307', '商务司机': '150208', '货运司机': '240301', '花艺师': '290701', '婚礼策划': '290702', '网吧网管': '290313', '验光师': '210109','服务员': '290202', '传菜员': '290216', '中餐厨师': '290219', '烧烤师傅': '290222', '西餐厨师': '290220', '日料厨师': '290221', '凉菜厨师': '290218', '面点师': '290213', '后厨': '290208', '配菜打荷': '290209', '洗碗工': '290217', '水台': '290224', '餐饮店长': '290206', '厨师长': '290215', '咖啡师': '290204', '茶艺师': '290210', '奶茶店店员': '290223', '调酒师': '290227', '餐饮学徒': '290212', '送餐员': '290205', '酒店前台': '290102', '客房服务员': '290103', '酒店经理': '290104', '酒店前厅经理': '290115', '客房经理': '290116', '民宿管家': '290158', '导游': '280104', '讲解员': '280106', '家教': '190321', '幼教': '190306', '托管老师': '190322', '早教老师': '190323', '小学教师': '190305', '初中教师': '190304', '高中教师': '190303', '篮球教练': '190706', '乒乓球教练': '190719', '足球教练': '190766', '羽毛球教练': '190720', '跆拳道教练': '190707', '武术教练': '190708', '轮滑教练': '190709', '书法教师': '190712', '播音主持教师': '190716', '表演教师': '190710', '钢琴教师': '190713', '古筝教师': '190715', '吉他教师': '190714', '架子鼓老师': '190767', '围棋老师': '190768', '乐高教师': '190717', '机器人教师': '190711', '少儿编程老师': '190718', '平面设计': '120106', '美工': '120117', 'UI设计师': '120105', '视觉设计师': '120101', '广告设计': '120108', '交互设计师': '120201', '网页设计师': '120102', '多媒体设计师': '120109', 'Flash设计师': '120103', '室内设计': '120607', '家具设计': '120604', '家居设计': '120605', '橱柜设计': '120603', '工业设计': '120602', '包装设计': '120118', '珠宝设计': '120606', 'threeD设计师': '120107', '插画师': '120121', '动画设计': '120120', '原画师': '120110', '漫画师': '120122', '修图师': '120123', '游戏场景': '120113', '游戏角色': '120114', '游戏界面设计师': '120112', '游戏特效': '120111', '游戏动作': '120115', '游戏主美术': '120306', '陈列设计': '120608', '照明设计': '120612', 'UX设计师': '120304', '工程造价': '220209', '工程监理': '220208', '工程预算': '220210', '施工员': '220218', '资料员': '220211', '材料员': '220220', '软装设计师': '220217', '建筑设计师': '220203', '建筑工程师': '220202', '城市规划设计': '220207', '弱电工程师': '220213', '建筑机电工程师': '220223', '给排水工程师': '220214', '暖通工程师': '220215', '幕墙工程师': '220216', 'BIM工程师': '220221', '消防工程师': '220224', '地产招投标': '220103', '地产项目管理': '220102', '房地产策划': '220101', '房产评估师': '220302', '主播': '170610', '剪辑师': '170623', '视频编辑': '170603', '后期制作': '170606', '编剧': '170616', '艺人助理': '170617', '制片人': '170615', '影视策划': '170609', '影视特效': '170624', '音频编辑': '170604', '灯光师': '170622', '放映员': '170613', '影视发行': '170608', '媒介投放': '140608', '媒介合作': '140609', '广告文案': '140605', '广告创意设计': '140601', '美术指导': '140602', '广告制作': '140607', '广告审核': '140611', '品牌公关': '140203', '活动策划执行': '140205', '媒介专员': '140204', '媒介经理': '140201', '媒介策划': '140206', '广告客户执行': '140202', '编辑': '170102', '校对录入': '170106', '印刷排版': '170109', '出版发行': '170105', '市场营销': '140101', '市场推广': '140104', '网络推广': '130109', '商务渠道': '140107', '市场策划': '140102', '活动策划': '140109', '市场顾问': '140103', '信息流优化师': '140116', 'SEO': '140105', 'SEM': '140106', 'APP推广': '140113', '游戏推广': '140115', '网络营销': '140110', '政府关系': '140112', '政策研究': '140801', '会展活动执行': '140506', '会议活动执行': '140503', '会展活动策划': '140505', '会议活动策划': '140502', '物流专员': '240103', '物流运营': '240105', '物流跟单': '240106', '调度员': '240108', '跟车员': '240119', '货运代理专员': '240111', '集装箱管理': '240302', '配送员': '240303', '快递员': '240304', '配送站长': '240118', '仓库管理员': '240204', '仓库文员': '240205', '供应链专员': '240101',  '采购工程师': '250105','招标专员': '250109', '投标专员': '250110', '贸易跟单': '250204', '单证员': '240117', '护士': '210201', '护士长': '210202', '外科医生': '210309', '内科医生': '210306', '皮肤科医生': '210313', '妇产科医生': '210311', '儿科医生': '210310', '眼科医生': '210312', '精神心理科医生': '210303', '整形医生': '210402', '全科医生': '210307', '耳鼻喉科医生': '210314', '检验科医师': '210111', '放射科医生': '210113', '超声科医生': '210114', '麻醉科医生': '210315', '病理科医生': '210316', '医生助理': '210112', '中医': '210302', '口腔科医生': '210304', '幼儿园保健医': '210308', '药剂师': '210104', '医务管理': '210317','康复治疗师': '210305', '生物学研究人员': '210115', '医药研发': '210108', '生物信息工程师': '210128', '药品生产': '210117', '药品注册': '210116', '医药项目经理': '210123', '药物分析': '210125', '制剂研发': '210129', '药物合成': '210126', '医疗产品技术支持': '210127','医疗器械研发': '210105', '医疗器械注册': '210121', '试剂研发': '210901', '柜员': '180402', '银行大堂经理': '180404', '信贷专员': '180406', '证券交易员': '180106', '卖方分析师': '180802', '买方分析师': '180803', '投资银行业务': '180806', '基金经理': '180805', '量化研究员': '180807', '合规稽查': '180204', '资信评估': '180203', '清算': '180304', '资产评估': '180104', '催收员': '180503', '投资经理': '180101', '投资助理': '180118', '行业研究': '180103', '融资': '180115', '投后管理': '180117', '并购': '180116', '保险理赔': '180703', '保险精算师': '180702','咨询项目管理': '260106', '企业管理咨询': '260101', '战略咨询': '260107', 'IT咨询顾问': '260104', '咨询经理': '260402', '人力资源咨询顾问': '260105', '猎头顾问': '260108', '咨询总监': '260401', '市场调研': '260109', '心理咨询师': '260112', '英语翻译': '260301', '日语翻译': '260302', '俄语翻译': '260306', '西班牙语翻译': '260307', '德语翻译': '260305', '法语翻译': '260304', '事务所律师': '260201', '律师助理': '260204', '专利律师': '150503', '知识产权律师': '260203', '光伏系统工程师': '301002', '风电运维工程': '301003', '水利工程师': '301004', '地质工程师': '301001', '饲养员': '400201', '畜牧兽医': '400203'}
