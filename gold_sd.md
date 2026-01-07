**背景信息：**
- **链接1**: https://apps.apple.com/us/app/gold-the-best-deals-daily/id6445965976 (这是一个XML格式的App Store页面，描述了GOLD应用的功能、用户评价、更新日志等细节)。
- **链接2**: https://jobs.ashbyhq.com/sagelabs.ai/67203763-323c-4ab2-bccb-efee374be78e(这是Sage AI Labs的招聘职位描述，强调AI驱动的个性化推荐系统、A/B测试平台等)。
- **链接3**: https://interviewing.io/guides/system-design-interview/part-three#about-this-3-step-framework (这是一个系统设计面试框架，详细介绍了需求分析、数据建模和设计步骤)。

**我的目标：**  
我正在面试Sage AI Labs公司（开发GOLD应用的公司），申请的是链接2中的AI Engineer岗位。系统设计轮面试要求是：“System Design (1 hour): Design high-level Architecture of systems emphasizing class structure, tradeoffs, scalability, concurrency, and caching—This will be a whiteboard session”。

**请求：**  
基于以上信息，请帮我完成以下任务：

1. **理解GOLD应用的工作原理**：根据链接1（App Store页面），详细总结GOLD应用是如何工作的。包括核心功能（如每日“Golden Hour”折扣、个性化推荐、AI学习用户偏好等）、用户流程、以及技术特点（如免费送货、无订阅费）。
   
2. **预测系统设计面试问题**：结合公司背景（Sage AI Labs专注于AI驱动的购物应用）和岗位要求（链接2），预测一个最有可能被问到的系统设计面试问题。问题应围绕GOLD应用的核心业务，例如设计一个个性化推荐系统或高并发交易平台。

3. **提供设计方案**：使用链接3中的3步框架（需求分析、数据/API/规模、设计）来回答预测的面试问题。设计方案必须全面符合公司背景（AI优先、电商规模）和工作描述（强调个性化、A/B测试、可扩展性）。方案需包括：
   - **类结构**（主要模块的职责和关系）。
   - **权衡分析**（如一致性vs.可用性、性能vs.成本）。
   - **可扩展性**（如何处理高并发、数据增长）。
   - **并发性**（如锁机制、队列使用）。
   - **缓存策略**（如Redis应用场景）。

4. **输出设计方案的详细内容**：对上述设计方案，提供：
   - **主要模块**：列出核心组件（如用户服务、推荐引擎、订单处理），并描述每个模块的职责。
   - **Mermaid架构图**：绘制一个高层架构图（使用Mermaid语法），展示模块间的交互和数据流，并解释图表。
   - **Mermaid序列图**：绘制一个序列图（使用Mermaid语法），以用户完成一次购买为例，展示端到端流程（如用户登录、接收推荐、下单、支付）。

